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

    user_id: int | None
    
    region_id: int
    
    region_name: str | None = None

    latitude: float

    longitude: float

    category: str

    severity: int

    description: str | None

    status: str
    
    confidence_score: float
    
    verification_count: int

    source: str

    timestamp: datetime

    class Config:
        from_attributes = True