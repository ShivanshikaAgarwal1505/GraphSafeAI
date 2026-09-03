from pathlib import Path

import pandas as pd

from shared.database.session import SessionLocal

from shared.database.models.safety_feature import (
    SafetyFeature
)

from shared.database.models.region_edge import (
    RegionEdge
)


def export_dataset():

    db = SessionLocal()

    output_dir = Path(
        "data/processed"
    )

    output_dir.mkdir(
        parents=True,
        exist_ok=True
    )

    # -------------------------
    # Safety Features
    # -------------------------

    features = (
        db.query(SafetyFeature)
        .all()
    )

    safety_rows = []

    for feature in features:

        safety_rows.append(
            {
                "region_id":
                    feature.region_id,

                "report_count":
                    feature.report_count,

                "avg_severity":
                    feature.avg_severity,

                "neighbor_report_count":
                    feature.neighbor_report_count,

                "neighbor_avg_severity":
                    feature.neighbor_avg_severity,

                "degree":
                    feature.degree,

                "safety_score":
                    feature.safety_score
            }
        )

    safety_df = pd.DataFrame(
        safety_rows
    )

    # -------------------------
    # Topology Features
    # -------------------------

    topology_df = pd.read_csv(
        output_dir /
        "topology_features.csv"
    )

    # -------------------------
    # Infrastructure Features
    # -------------------------

    infrastructure_df = pd.read_csv(
        output_dir /
        "infrastructure_features.csv"
    )

    # -------------------------
    # Merge Features
    # -------------------------

    node_df = (
        safety_df
        .merge(
            topology_df,
            on="region_id",
            how="left"
        )
        .merge(
            infrastructure_df,
            on="region_id",
            how="left"
        )
    )

    node_df.fillna(
        0,
        inplace=True
    )

    node_path = (
        output_dir /
        "node_features.csv"
    )

    node_df.to_csv(
        node_path,
        index=False
    )

    # -------------------------
    # Edge List
    # -------------------------

    edges = (
        db.query(RegionEdge)
        .all()
    )

    edge_rows = []

    for edge in edges:

        edge_rows.append(
            {
                "source_region_id":
                    edge.source_region_id,

                "target_region_id":
                    edge.target_region_id
            }
        )

    edge_df = pd.DataFrame(
        edge_rows
    )

    edge_path = (
        output_dir /
        "edge_list.csv"
    )

    edge_df.to_csv(
        edge_path,
        index=False
    )

    db.close()

    print(
        f"Nodes exported: {len(node_df)}"
    )

    print(
        f"Edges exported: {len(edge_df)}"
    )

    print(
        f"Feature columns: {len(node_df.columns)}"
    )

    print(
        f"Saved -> {output_dir}"
    )


if __name__ == "__main__":
    export_dataset()