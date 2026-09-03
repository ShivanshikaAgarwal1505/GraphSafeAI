from pathlib import Path

import pandas as pd

from shared.database.session import SessionLocal

from shared.database.models.region import Region
from shared.database.models.region_edge import RegionEdge
from shared.database.models.safety_feature import SafetyFeature


def populate_regions():

    db = SessionLocal()

    # delete child tables first

    db.query(
        SafetyFeature
    ).delete()

    db.commit()

    db.query(
        RegionEdge
    ).delete()

    db.commit()

    db.query(
        Region
    ).delete()

    db.commit()

    regions_df = pd.read_csv(
        Path(
            "data/processed/regions.csv"
        )
    )

    for _, row in regions_df.iterrows():

        db.add(
            Region(
                id=int(row["region_id"]),
                region_name=
                    f"OSM_REGION_{int(row['region_id'])}",
                centroid_lat=float(
                    row["center_lat"]
                ),
                centroid_lon=float(
                    row["center_lon"]
                ),
                safety_score=0.5
            )
        )

    db.commit()

    print(
        f"Inserted {len(regions_df)} regions"
    )

    db.close()


if __name__ == "__main__":
    populate_regions()