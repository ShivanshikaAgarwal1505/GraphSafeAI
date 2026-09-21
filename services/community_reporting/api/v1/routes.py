from shared.database import current_user
from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException

from sqlalchemy.orm import Session

from shared.database.dependency import get_db

from shared.schemas.report_schema import (
    CommunityReportCreate,
    CommunityReportResponse
)

from services.community_reporting.application.report_service import (
    ReportService
)

from services.community_reporting.application.category_service import (
    CategoryService
)

from shared.database.current_user import (
    get_current_user,
)

from shared.database.models.user import (
    User,
)

router = APIRouter()

service = ReportService()

category_service = CategoryService()


@router.post("/")
def create_report(
    report: CommunityReportCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(
        get_current_user,
    ),
):

    saved_report = service.create_report(
        db=db,
        report_data=report,
        user_id=current_user.id,
    )

    return {
        "id": saved_report.id,
        "message": "Report saved successfully",
    }


@router.get(
    "",
    response_model=list[
        CommunityReportResponse
    ]
)
def get_reports(
    status: str | None = None,
    category: str | None = None,
    region_id: int | None = None,
    source: str | None = None,
    db: Session = Depends(get_db)
):

    return service.get_reports(
        db=db,
        status=status,
        category=category,
        region_id=region_id,
        source=source
    )

@router.get("/my")
def my_reports(
    db: Session = Depends(get_db),
    current_user: User = Depends(
        get_current_user,
    ),
):
    return service.get_my_reports(
        db=db,
        user_id=current_user.id,
    )
    
@router.get(
    "/{report_id}",
    response_model=CommunityReportResponse
)
def get_report(
    report_id: int,
    db: Session = Depends(get_db)
):

    try:

        return service.get_report(
            db,
            report_id
        )

    except ValueError as exc:

        raise HTTPException(
            status_code=404,
            detail=str(exc)
        )


@router.patch(
    "/{report_id}/resolve"
)
def resolve_report(
    report_id: int,
    db: Session = Depends(get_db)
):

    report = (
        service.resolve_report(
            db,
            report_id
        )
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

    report = (
        service.reopen_report(
            db,
            report_id
        )
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

    report = (
        service.reject_report(
            db,
            report_id
        )
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

    return category_service.get_categories(
        db
    )


@router.get(
    "/categories/stats"
)
def get_category_stats(
    db: Session = Depends(get_db)
):

    return category_service.get_category_stats(
        db
    )
    
@router.get(
    "/regions/{region_id}"
)
def get_region_stats(
    region_id: int,
    db: Session = Depends(get_db)
):

    return service.get_region_stats(
        db,
        region_id
    )
    
@router.get("/health")
def health():

    return {
        "status": "healthy"
    }

@router.patch("/{report_id}/close")
def close_report(
    report_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(
        get_current_user,
    ),
):
    try:
        report = service.close_report(
            db=db,
            report_id=report_id,
            user_id=current_user.id,
        )

        return {
            "id": report.id,
            "status": report.status,
        }

    except PermissionError as exc:
        raise HTTPException(
            status_code=403,
            detail=str(exc),
        )