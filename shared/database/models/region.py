from sqlalchemy import Column, Float, Integer, String

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