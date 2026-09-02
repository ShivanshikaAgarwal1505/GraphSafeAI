from shared.database.database import engine

from shared.database.models.base import Base

from shared.database.models.region import Region
from shared.database.models.community_report import CommunityReport
from shared.database.models.region_edge import RegionEdge


def create_tables():
    Base.metadata.create_all(bind=engine)


if __name__ == "__main__":
    create_tables()

    print("Database tables created.")