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