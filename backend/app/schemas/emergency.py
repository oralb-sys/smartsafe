from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel, Field


class EmergencyCreateResponse(BaseModel):
    id: str
    status: str
    created_at: datetime


class EmergencyLocationRequest(BaseModel):
    latitude: Decimal = Field(
        ge=-90,
        le=90,
    )

    longitude: Decimal = Field(
        ge=-180,
        le=180,
    )


class EmergencyLocationResponse(BaseModel):
    id: str
    latitude: Decimal
    longitude: Decimal
    status: str