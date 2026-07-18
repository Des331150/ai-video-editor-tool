import uuid

from pydantic import BaseModel, ConfigDict


class TranscriptEntryResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    word: str
    start_time: float
    end_time: float
    position: int


class TranscriptResponse(BaseModel):
    source_id: uuid.UUID
    entries: list[TranscriptEntryResponse]
