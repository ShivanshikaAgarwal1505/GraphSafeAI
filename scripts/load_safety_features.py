import pandas as pd

from shared.database.session import SessionLocal
from shared.database.models.region import Region
from shared.database.models.safety_feature import (
    SafetyFeature
)


def main():

    db = SessionLocal()

    db.query(
        SafetyFeature
    ).delete()

    db.commit()

    df = pd.read_csv(
        "data/processed/node_features.csv"
    )

    for _, row in df.iterrows():

        db.add(
            SafetyFeature(
                region_id=int(
                    row["region_id"]
                ),
                report_count=int(
                    row["report_count"]
                ),
                avg_severity=float(
                    row["avg_severity"]
                ),
                neighbor_report_count=0,
                neighbor_avg_severity=0,
                degree=float(
                    row["avg_degree"]
                ),
                safety_score=float(
                    row["safety_score"]
                )
            )
        )

    db.commit()

    print(
        f"Inserted {len(df)} features"
    )

    db.close()


if __name__ == "__main__":
    main()