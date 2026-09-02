from fastapi import APIRouter
from fastapi import Depends

from sqlalchemy.orm import Session

from shared.database.dependency import get_db

from shared.schemas.report_schema import (
    CommunityReportCreate
)

from services.community_reporting.application.report_service import (
    ReportService
)

router = APIRouter()

service = ReportService()


@router.post("/")
def create_report(
    report: CommunityReportCreate,
    db: Session = Depends(get_db)
):
    saved_report = service.create_report(
        db=db,
        report_data=report
    )

    return {
        "id": saved_report.id,
        "message": "Report saved successfully"
    }