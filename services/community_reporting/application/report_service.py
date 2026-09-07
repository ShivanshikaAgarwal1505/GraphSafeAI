from sqlalchemy.orm import Session

from shared.database.models.community_report import (
    CommunityReport
)

from shared.geo.region_mapper import (
    RegionMapper
)

from services.community_reporting.infrastructure.report_repository import (
    ReportRepository
)

from services.safety_intelligence.application.risk_refresh_service import (
    RiskRefreshService
)

repository = ReportRepository()

risk_service = RiskRefreshService()

class ReportService:

    def __init__(self):

        self.region_mapper = (
            RegionMapper()
        )

    def create_report(
        self,
        db: Session,
        report_data
    ):

        region_id = (
            self.region_mapper.find_region(
                latitude=report_data.latitude,
                longitude=report_data.longitude
            )
        )

        if region_id is None:

            raise ValueError(
                "Region not found."
            )

        report = CommunityReport(

            region_id=region_id,

            latitude=report_data.latitude,

            longitude=report_data.longitude,

            category=report_data.category,

            severity=report_data.severity,

            description=report_data.description,

            source=report_data.source,

            status="OPEN",

            timestamp=report_data.timestamp
        )

        saved_report = (
            repository.create(
                db=db,
                report=report
            )
        )

        return saved_report

    def resolve_report(
        self,
        db,
        report_id: int
    ):

        report = repository.get(
            db,
            report_id
        )

        if report is None:
            raise ValueError(
                "Report not found"
            )

        report.status = "RESOLVED"

        repository.save(db)

        return report

    def reopen_report(
        self,
        db,
        report_id: int
    ):

        report = repository.get(
            db,
            report_id
        )

        if report is None:
            raise ValueError(
                "Report not found"
            )

        report.status = "OPEN"

        repository.save(db)

        return report

    def reject_report(
        self,
        db,
        report_id: int
    ):

        report = repository.get(
            db,
            report_id
        )

        if report is None:
            raise ValueError(
                "Report not found"
            )

        report.status = "REJECTED"

        repository.save(db)

        return report