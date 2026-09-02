from shared.database.session import SessionLocal

from shared.database.models.region import Region
from shared.database.models.region_edge import RegionEdge


ROWS = 11
COLS = 21


def build_graph():

    db = SessionLocal()

    existing_edges = db.query(RegionEdge).count()

    if existing_edges > 0:
        print(
            f"Graph already exists ({existing_edges} edges)."
        )
        db.close()
        return

    regions = (
        db.query(Region)
        .order_by(Region.id)
        .all()
    )

    print(f"Loaded {len(regions)} regions")

    edge_count = 0

    for row in range(ROWS):

        for col in range(COLS):

            current_index = row * COLS + col

            current_id = regions[current_index].id

            # right neighbor
            if col < COLS - 1:

                right_id = regions[current_index + 1].id

                db.add(
                    RegionEdge(
                        source_region_id=current_id,
                        target_region_id=right_id
                    )
                )

                edge_count += 1

            # bottom neighbor
            if row < ROWS - 1:

                bottom_id = regions[current_index + COLS].id

                db.add(
                    RegionEdge(
                        source_region_id=current_id,
                        target_region_id=bottom_id
                    )
                )

                edge_count += 1

    db.commit()

    print(f"Created {edge_count} edges")

    db.close()


if __name__ == "__main__":
    build_graph()