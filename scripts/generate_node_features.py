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

    merged = nodes.merge(
        mapping,
        on="node_id"
    )

    degree_map = {}

    for _, row in edges.iterrows():

        source = row["source"]
        target = row["target"]

        degree_map[source] = (
            degree_map.get(source, 0) + 1
        )

        degree_map[target] = (
            degree_map.get(target, 0) + 1
        )

    merged["degree"] = (
        merged["node_id"]
        .map(degree_map)
        .fillna(0)
    )

    region_features = (
        merged.groupby("region_id")
        .agg(
            node_count=(
                "node_id",
                "count"
            ),

            avg_degree=(
                "degree",
                "mean"
            ),

            dead_end_count=(
                "degree",
                lambda x: (x == 1).sum()
            ),

            intersection_count=(
                "degree",
                lambda x: (x >= 3).sum()
            )
        )
        .reset_index()
    )

    region_features[
        "dead_end_ratio"
    ] = (
        region_features[
            "dead_end_count"
        ]
        /
        region_features[
            "node_count"
        ]
    )

    region_features[
        "intersection_density"
    ] = (
        region_features[
            "intersection_count"
        ]
        /
        region_features[
            "node_count"
        ]
    )

    region_features[
        "connectivity_score"
    ] = (
        region_features[
            "avg_degree"
        ]
        /
        region_features[
            "avg_degree"
        ].max()
    )

    region_features.to_csv(
        "data/processed/topology_features.csv",
        index=False
    )

    print(
        f"Features: {len(region_features)}"
    )


if __name__ == "__main__":
    main()