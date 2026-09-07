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

    high_severity_count = Column(
        Integer,
        default=0
    )

    recent_report_count = Column(
        Integer,
        default=0
    )

    incident_diversity = Column(
        Integer,
        default=0
    )

    neighbor_incident_diversity = Column(
        Float,
        default=0
    )

    # category features

    theft_count = Column(Integer, default=0)

    harassment_count = Column(Integer, default=0)

    accident_count = Column(Integer, default=0)

    unsafe_area_count = Column(Integer, default=0)

    streetlight_failure_count = Column(
        Integer,
        default=0
    )

    # temporal features

    reports_last_7_days = Column(
        Integer,
        default=0
    )

    reports_last_30_days = Column(
        Integer,
        default=0
    )

    reports_last_90_days = Column(
        Integer,
        default=0
    )

    incident_growth_rate = Column(
        Float,
        default=0
    )

    structural_risk = Column(
        Float,
        default=0
    )

    incident_risk = Column(
        Float,
        default=0
    )

    incident_confidence = Column(
        Float,
        default=0
    )

    structural_weight = Column(
        Float,
        default=1
    )

    incident_weight = Column(
        Float,
        default=0
    )

    final_risk = Column(
        Float,
        default=0
    )