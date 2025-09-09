from pydantic import BaseModel
from typing import Optional
from datetime import datetime
import uuid

class AudioFileBase(BaseModel):
    filename: str
    content_type: str
    size: int

class AudioFileCreate(AudioFileBase):
    pass

class AudioFile(AudioFileBase):
    id: str  # UUID or timestamp-based identifier
    upload_timestamp: datetime
    storage_path: str

    class Config:
        from_attributes = True
