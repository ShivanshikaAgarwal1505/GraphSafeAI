from sqlalchemy import Column
from sqlalchemy import ForeignKey
from sqlalchemy import Integer

from shared.database.models.base import Base


class RegionEdge(Base):
    __tablename__ = "region_edges"

    id = Column(Integer, primary_key=True)

    source_region_id = Column(
        Integer,
        ForeignKey("regions.id"),
        nullable=False
    )

    target_region_id = Column(
        Integer,
        ForeignKey("regions.id"),
        nullable=False
    )