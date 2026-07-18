import os
import shutil
import uuid
from pathlib import Path

from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.config import settings
from app.database import get_db
from app.dependencies import get_project_or_404, get_transcriber
from app.models.source_media import SourceMedia
from app.models.transcript import TranscriptEntry
from app.schemas.source_media import SourceMediaResponse
from app.services.transcriber import Transcriber

router = APIRouter(prefix="/api/projects/{project_id}/sources", tags=["sources"])

VIDEO_EXTENSIONS = {".mp4", ".mov", ".avi", ".mkv", ".webm", ".m4v"}
AUDIO_EXTENSIONS = {".mp3", ".wav", ".aac", ".ogg", ".flac", ".wma", ".m4a"}
ALL_MEDIA_EXTENSIONS = VIDEO_EXTENSIONS | AUDIO_EXTENSIONS


def _classify_media_type(filename: str) -> str:
    ext = Path(filename).suffix.lower()
    return "video" if ext in VIDEO_EXTENSIONS else "audio"


async def _get_source_or_404(
    source_id: uuid.UUID, project_id: uuid.UUID, db: AsyncSession
) -> SourceMedia:
    result = await db.execute(
        select(SourceMedia).where(
            SourceMedia.id == source_id, SourceMedia.project_id == project_id
        )
    )
    source = result.scalar_one_or_none()
    if source is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Source not found")
    return source


@router.get("", response_model=list[SourceMediaResponse])
async def list_sources(
    project_id: uuid.UUID,
    db: AsyncSession = Depends(get_db),
    project=Depends(get_project_or_404),
):
    result = await db.execute(
        select(SourceMedia)
        .where(SourceMedia.project_id == project_id)
        .order_by(SourceMedia.created_at.desc())
    )
    return result.scalars().all()


@router.post("", response_model=SourceMediaResponse, status_code=status.HTTP_201_CREATED)
async def upload_source(
    project_id: uuid.UUID,
    file: UploadFile = File(...),
    duration: float | None = Form(None),
    db: AsyncSession = Depends(get_db),
    project=Depends(get_project_or_404),
    transcriber: Transcriber = Depends(get_transcriber),
):
    if not file.filename:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Filename is required")

    ext = Path(file.filename).suffix.lower()
    if ext not in ALL_MEDIA_EXTENSIONS:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Unsupported media extension: {ext}",
        )

    source_id = uuid.uuid4()

    source = SourceMedia(
        id=source_id,
        project_id=project_id,
        filename=file.filename,
        file_path="",
        duration=duration,
        file_size=0,
        media_type=_classify_media_type(file.filename),
    )
    db.add(source)
    await db.flush()

    storage_dir = Path(settings.storage_path)
    storage_dir.mkdir(parents=True, exist_ok=True)
    stored_filename = f"{source_id}{ext}"
    stored_path = storage_dir / stored_filename

    try:
        with open(stored_path, "wb") as f:
            shutil.copyfileobj(file.file, f)

        file_stat = os.stat(stored_path)
        source.file_path = str(stored_path)
        source.file_size = file_stat.st_size
        await db.flush()
        await db.refresh(source)

        words = await transcriber.transcribe(str(stored_path))
        for i, wt in enumerate(words):
            entry = TranscriptEntry(
                source_id=source.id,
                word=wt.word,
                start_time=wt.start_time,
                end_time=wt.end_time,
                position=i,
            )
            db.add(entry)
        await db.flush()
    except Exception:
        if stored_path.exists():
            stored_path.unlink()
        raise

    return source


@router.delete("/{source_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_source(
    project_id: uuid.UUID,
    source_id: uuid.UUID,
    db: AsyncSession = Depends(get_db),
    project=Depends(get_project_or_404),
):
    result = await db.execute(
        select(SourceMedia).where(
            SourceMedia.id == source_id, SourceMedia.project_id == project_id
        )
    )
    source = result.scalar_one_or_none()
    if source is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Source not found")

    stored_path = Path(source.file_path)
    if stored_path.exists():
        stored_path.unlink()

    await db.delete(source)
    await db.flush()
