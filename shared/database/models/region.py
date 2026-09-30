from sqlalchemy import Column
from sqlalchemy import Float
from sqlalchemy import Integer
from sqlalchemy import String

from shared.database.models.base import Base


class Region(Base):
    __tablename__ = "regions"

    id = Column(Integer, primary_key=True)

    region_name = Column(
        String(100),
        nullable=False
    )

    centroid_lat = Column(
        Float,
        nullable=False
    )

    centroid_lon = Column(
        Float,
        nullable=False
    )

    safety_score = Column(
        Float,
        nullable=False,
        default=0.5
    )