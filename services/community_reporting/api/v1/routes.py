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

@router.patch(
    "/{report_id}/resolve"
)
def resolve_report(
    report_id: int,
    db: Session = Depends(get_db)
):

    report = service.resolve_report(
        db,
        report_id
    )

    return {
        "id": report.id,
        "status": report.status
    }


@router.patch(
    "/{report_id}/reopen"
)
def reopen_report(
    report_id: int,
    db: Session = Depends(get_db)
):

    report = service.reopen_report(
        db,
        report_id
    )

    return {
        "id": report.id,
        "status": report.status
    }


@router.patch(
    "/{report_id}/reject"
)
def reject_report(
    report_id: int,
    db: Session = Depends(get_db)
):

    report = service.reject_report(
        db,
        report_id
    )

    return {
        "id": report.id,
        "status": report.status
    }

@router.get(
    "/categories"
)
def get_categories(
    db: Session = Depends(get_db)
):

    service = CategoryService()

    return service.get_categories(db)