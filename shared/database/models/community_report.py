from sqlalchemy import (
    Column,
    DateTime,
    Float,
    ForeignKey,
    Integer,
    String
)

from datetime import datetime

from shared.database.models.base import Base


class CommunityReport(Base):

    __tablename__ = "community_reports"

    id = Column(
        Integer,
        primary_key=True
    )

    region_id = Column(
        Integer,
        ForeignKey(
            "regions.id"
        ),
        nullable=False
    )

    user_id = Column(
        Integer,
        ForeignKey("users.id"),
        nullable=True,
    )
    
    latitude = Column(
        Float,
        nullable=False
    )

    longitude = Column(
        Float,
        nullable=False
    )

    category = Column(
        String(100),
        nullable=False
    )

    severity = Column(
        Integer,
        nullable=False
    )

    description = Column(
        String(1000),
        nullable=True
    )

    status = Column(
        String(50),
        nullable=False,
        default="OPEN"
    )

    confidence_score = Column(
        Float,
        nullable=False,
        default=0.0,
    )

    verification_count = Column(
        Integer,
        nullable=False,
        default=0,
    )

    source = Column(
        String(50),
        nullable=False,
        default="CITIZEN"
    )

    created_at = Column(
        DateTime,
        default=datetime.utcnow
    )

    updated_at = Column(
        DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow
    )

    timestamp = Column(
        DateTime,
        nullable=False
    )