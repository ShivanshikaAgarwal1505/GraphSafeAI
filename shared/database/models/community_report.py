from sqlalchemy import (
    Column,
    DateTime,
    Float,
    Integer,
    String
)

from shared.database.models.base import Base


class CommunityReport(Base):
    __tablename__ = "community_reports"

    id = Column(Integer, primary_key=True)

    latitude = Column(Float, nullable=False)

    longitude = Column(Float, nullable=False)

    category = Column(
        String(100),
        nullable=False
    )

    severity = Column(
        Integer,
        nullable=False
    )

    timestamp = Column(
        DateTime,
        nullable=False
    )