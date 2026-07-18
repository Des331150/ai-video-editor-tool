import uuid

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.dependencies import get_project_or_404
from app.models.source_media import SourceMedia
from app.models.transcript import TranscriptEntry
from app.schemas.transcript import TranscriptResponse

router = APIRouter(prefix="/api/projects/{project_id}/sources", tags=["transcripts"])


@router.get(
    "/{source_id}/transcript",
    response_model=TranscriptResponse,
)
async def get_transcript(
    project_id: uuid.UUID,
    source_id: uuid.UUID,
    db: AsyncSession = Depends(get_db),
    project=Depends(get_project_or_404),
):
    source_result = await db.execute(
        select(SourceMedia).where(
            SourceMedia.id == source_id, SourceMedia.project_id == project_id
        )
    )
    if source_result.scalar_one_or_none() is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Source not found"
        )

    result = await db.execute(
        select(TranscriptEntry)
        .where(TranscriptEntry.source_id == source_id)
        .order_by(TranscriptEntry.position)
    )
    entries = result.scalars().all()
    return TranscriptResponse(source_id=source_id, entries=entries)
