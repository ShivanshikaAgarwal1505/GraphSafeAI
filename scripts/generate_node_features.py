import pandas as pd


def main():

    nodes = pd.read_csv(
        "data/processed/osm_nodes_v2.csv"
    )

    edges = pd.read_csv(
        "data/processed/osm_edges_v2.csv"
    )

    mapping = pd.read_csv(
        "data/processed/node_region_map.csv"
    )

    merged = (
        nodes.merge(
            mapping,
            on="node_id"
        )
    )

    degree_map = {}

    for _, row in edges.iterrows():

        degree_map[
            row["source"]
        ] = (
            degree_map.get(
                row["source"],
                0
            )
            + 1
        )

        degree_map[
            row["target"]
        ] = (
            degree_map.get(
                row["target"],
                0
            )
            + 1
        )

    merged["degree"] = (
        merged["node_id"]
        .map(degree_map)
        .fillna(0)
    )

    region_features = (
        merged.groupby(
            "region_id"
        )
        .agg(
            node_count=(
                "node_id",
                "count"
            ),
            avg_degree=(
                "degree",
                "mean"
            )
        )
        .reset_index()
    )

    region_features[
        "report_count"
    ] = 0

    region_features[
        "avg_severity"
    ] = 0

    region_features[
        "neighbor_score"
    ] = (
        region_features[
            "avg_degree"
        ]
        /
        region_features[
            "avg_degree"
        ].max()
    )

    region_features[
        "safety_score"
    ] = (
        0.5
        + 0.5
        * region_features[
            "neighbor_score"
        ]
    )

    region_features.to_csv(
        "data/processed/node_features.csv",
        index=False
    )

    print(
        f"Features: {len(region_features)}"
    )


if __name__ == "__main__":
    main()