from shared.database.session import SessionLocal

from shared.database.models.region import Region
from shared.database.models.region_edge import RegionEdge


def test_graph():

    db = SessionLocal()

    region_count = db.query(Region).count()
    edge_count = db.query(RegionEdge).count()

    print(f"Regions: {region_count}")
    print(f"Edges: {edge_count}")

    db.close()


if __name__ == "__main__":
    test_graph()