import uuid
from datetime import datetime

from pydantic import BaseModel, ConfigDict


class SourceMediaResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    project_id: uuid.UUID
    filename: str
    duration: float | None
    file_size: int
    media_type: str
    created_at: datetime
