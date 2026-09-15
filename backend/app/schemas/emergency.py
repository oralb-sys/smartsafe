from datetime import datetime

from pydantic import BaseModel


class EmergencyCreateResponse(BaseModel):
    id: str
    status: str
    created_at: datetime