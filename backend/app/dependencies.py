import uuid

from fastapi import Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.config import settings
from app.database import get_db
from app.models.project import Project
from app.services.transcriber import FakeTranscriber, Transcriber, WhisperTranscriber


async def get_project_or_404(
    project_id: uuid.UUID,
    db: AsyncSession = Depends(get_db),
) -> Project:
    result = await db.execute(select(Project).where(Project.id == project_id))
    project = result.scalar_one_or_none()
    if project is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Project not found")
    return project


def get_transcriber() -> Transcriber:
    if settings.transcriber_type == "whisper":
        return WhisperTranscriber()
    return FakeTranscriber()
