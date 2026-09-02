from sqlalchemy import Column
from sqlalchemy import Float
from sqlalchemy import ForeignKey
from sqlalchemy import Integer

from shared.database.models.base import Base

class SafetyFeature(Base):
    __tablename__ = "safety_features"

    id = Column(Integer, primary_key=True)

    region_id = Column(
        Integer,
        ForeignKey("regions.id"),
        nullable=False
    )

    report_count = Column(Integer, default=0)

    avg_severity = Column(Float, default=0)

    neighbor_report_count = Column(
        Float,
        default=0
    )

    neighbor_avg_severity = Column(
        Float,
        default=0
    )

    degree = Column(
        Integer,
        default=0
    )

    safety_score = Column(
        Float,
        default=0.5
    )