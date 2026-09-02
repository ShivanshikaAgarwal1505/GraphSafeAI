from datetime import datetime

from pydantic import BaseModel

from shared.enums.report_category import ReportCategory


class CommunityReportCreate(BaseModel):
    latitude: float
    longitude: float
    category: ReportCategory
    severity: int
    timestamp: datetime