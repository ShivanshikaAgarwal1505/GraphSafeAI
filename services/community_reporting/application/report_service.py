from sqlalchemy.orm import Session

from shared.database.models.community_report import CommunityReport

from services.community_reporting.infrastructure.report_repository import (
    ReportRepository
)

repository = ReportRepository()


class ReportService:

    def create_report(
        self,
        db: Session,
        report_data
    ):
        report = CommunityReport(
            latitude=report_data.latitude,
            longitude=report_data.longitude,
            category=report_data.category.value,
            severity=report_data.severity,
            timestamp=report_data.timestamp
        )

        return repository.create(
            db=db,
            report=report
        )