from datetime import datetime
from decimal import Decimal
from typing import Literal

from pydantic import BaseModel, Field


ReportCategory = Literal[
    "POTHOLE",
    "WASTE",
    "STREET_LIGHT",
    "WATER_LEAK",
]


class ReportCreateRequest(BaseModel):
    category: ReportCategory
    description: str | None = Field(default=None, max_length=2000)
    latitude: Decimal = Field(ge=-90, le=90)
    longitude: Decimal = Field(ge=-180, le=180)
    photo_url: str | None = Field(default=None, max_length=500)


class ReportCreateResponse(BaseModel):
    id: str
    category: str
    description: str | None
    latitude: Decimal
    longitude: Decimal
    photo_url: str | None
    status: str
    created_at: datetime
