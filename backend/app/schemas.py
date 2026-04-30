from pydantic import BaseModel, HttpUrl
from datetime import datetime
from typing import Optional

class QRCodeBase(BaseModel):
    original_url: HttpUrl
    expires_at: Optional[datetime] = None

class QRCodeCreate(QRCodeBase):
    pass

class QRCodeUpdate(BaseModel):
    original_url: Optional[HttpUrl] = None
    expires_at: Optional[datetime] = None

class QRCode(QRCodeBase):
    id: int
    short_token: str
    created_at: datetime
    updated_at: Optional[datetime] = None
    deleted_at: Optional[datetime] = None

    class Config:
        from_attributes = True