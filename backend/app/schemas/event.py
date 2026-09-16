from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel


class UrbanEventResponse(BaseModel):
    id: str
    source: str
    type: str
    status: str
    description: str | None
    latitude: Decimal | None
    longitude: Decimal | None
    photo_url: str | None
    created_at: datetime