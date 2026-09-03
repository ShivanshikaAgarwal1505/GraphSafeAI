import pandas as pd

from shared.database.session import SessionLocal
from shared.database.models.region_edge import RegionEdge


def build_graph():

    db = SessionLocal()

    db.query(RegionEdge).delete()
    db.commit()

    edges_df = pd.read_csv(
        "data/processed/edge_list.csv"
    )

    edge_count = 0

    for _, row in edges_df.iterrows():

        db.add(
            RegionEdge(
                source_region_id=int(
                    row["source"]
                ),
                target_region_id=int(
                    row["target"]
                )
            )
        )

        edge_count += 1

    db.commit()

    print(
        f"Inserted {edge_count} edges"
    )

    db.close()


if __name__ == "__main__":
    build_graph()