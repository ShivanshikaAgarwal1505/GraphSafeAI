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

    def save(
        self,
        db: Session
    ):

        db.commit()