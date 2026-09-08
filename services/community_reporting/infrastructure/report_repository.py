from sqlalchemy.orm import Session

from shared.database.models.community_report import (
    CommunityReport
)


class ReportRepository:

    def create(
        self,
        db: Session,
        report: CommunityReport
    ):

        db.add(report)

        db.commit()

        db.refresh(report)

        return report

    def get(
        self,
        db: Session,
        report_id: int
    ):

        return (
            db.query(
                CommunityReport
            )
            .filter(
                CommunityReport.id
                == report_id
            )
            .first()
        )

    def get_all(
        self,
        db: Session
    ):

        return (
            db.query(
                CommunityReport
            )
            .all()
        )

    def get_filtered(
        self,
        db: Session,
        status=None,
        category=None,
        region_id=None,
        source=None
    ):

        query = db.query(
            CommunityReport
        )

        if status:

            query = query.filter(
                CommunityReport.status
                == status
            )

        if category:

            query = query.filter(
                CommunityReport.category
                == category
            )

        if region_id:

            query = query.filter(
                CommunityReport.region_id
                == region_id
            )

        if source:

            query = query.filter(
                CommunityReport.source
                == source
            )

        return query.all()

    def save(
        self,
        db: Session
    ):

        db.commit()