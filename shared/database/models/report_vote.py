from datetime import datetime

from sqlalchemy import (
    Column,
    DateTime,
    ForeignKey,
    Integer,
    String,
)

from shared.database.models.base import Base


class ReportVote(Base):

    __tablename__ = "report_votes"

    id = Column(
        Integer,
        primary_key=True,
    )

    report_id = Column(
        Integer,
        ForeignKey(
            "community_reports.id",
        ),
        nullable=False,
    )

    user_id = Column(
        Integer,
        ForeignKey(
            "users.id",
        ),
        nullable=False,
    )

    vote_type = Column(
        String(20),
        nullable=False,
    )

    created_at = Column(
        DateTime,
        default=datetime.utcnow,
    )