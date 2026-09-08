from datetime import datetime

from pydantic import BaseModel


class CommunityReportCreate(
    BaseModel
):

    latitude: float

    longitude: float

    category: str

    severity: int

    description: str | None = None

    source: str = "CITIZEN"

    timestamp: datetime


class CommunityReportResponse(
    BaseModel
):

    id: int

    region_id: int

    latitude: float

    longitude: float

    category: str

    severity: int

    description: str | None

    status: str

    source: str

    timestamp: datetime

    class Config:
        from_attributes = True