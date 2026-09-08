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

from shared.database.models.region import Region

repository = ReportRepository()

refresh_service = RiskRefreshService()

class ReportService:

    def __init__(self):

        self.region_mapper = (
            RegionMapper()
        )

        self.refresh_service = (
            RiskRefreshService()
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


        saved_report = repository.create(
            db=db,
            report=report
        )

        refresh_service.refresh_region_and_neighbors(
            db,
            saved_report.region_id
        )

        return saved_report

    def get_report(
        self,
        db: Session,
        report_id: int
    ):

        report = repository.get(
            db,
            report_id
        )

        if report is None:

            raise ValueError(
                "Report not found."
            )

        return report

    def get_reports(
        self,
        db: Session
    ):

        return repository.get_all(db)

    def resolve_report(
        self,
        db: Session,
        report_id: int
    ):

        report = self.get_report(
            db,
            report_id
        )

        report.status = "RESOLVED"

        repository.save(db)

        return report

    def reopen_report(
        self,
        db: Session,
        report_id: int
    ):

        report = self.get_report(
            db,
            report_id
        )

        report.status = "OPEN"

        repository.save(db)

        return report

    def reject_report(
        self,
        db: Session,
        report_id: int
    ):

        report = self.get_report(
            db,
            report_id
        )

        report.status = "REJECTED"

        repository.save(db)

        return report

    def get_reports(
        self,
        db,
        status=None,
        category=None,
        region_id=None,
        source=None
    ):

        return repository.get_filtered(
            db=db,
            status=status,
            category=category,
            region_id=region_id,
            source=source
        )

    def get_region_stats(
        self,
        db,
        region_id
    ):

        reports = repository.get_filtered(
            db=db,
            region_id=region_id
        )

        categories = {}

        open_count = 0

        resolved_count = 0

        rejected_count = 0

        for report in reports:

            categories[
                report.category
            ] = (

                categories.get(
                    report.category,
                    0
                )
                + 1

            )

            if report.status == "OPEN":

                open_count += 1

            elif report.status == "RESOLVED":

                resolved_count += 1

            elif report.status == "REJECTED":

                rejected_count += 1

        return {

            "region_id": region_id,

            "report_count":
                len(reports),

            "open_reports":
                open_count,

            "resolved_reports":
                resolved_count,

            "rejected_reports":
                rejected_count,

            "categories":
                categories,
        }