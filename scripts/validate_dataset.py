from pathlib import Path

import pandas as pd


def main():

    processed = Path(
        "data/processed"
    )

    node_df = pd.read_csv(
        processed /
        "node_features.csv"
    )

    edge_df = pd.read_csv(
        processed /
        "edge_list.csv"
    )

    print()
    print("DATASET VALIDATION")
    print("=" * 50)

    print()
    print(
        f"Regions: {len(node_df)}"
    )

    print(
        f"Edges: {len(edge_df)}"
    )

    print()

    duplicate_regions = (
        node_df["region_id"]
        .duplicated()
        .sum()
    )

    print(
        f"Duplicate Regions: {duplicate_regions}"
    )

    null_values = (
        node_df
        .isnull()
        .sum()
        .sum()
    )

    print(
        f"Null Values: {null_values}"
    )

    distance_columns = [
        c
        for c in node_df.columns
        if c.startswith(
            "nearest_"
        )
    ]

    negative_distances = 0

    for col in distance_columns:

        negative_distances += (
            node_df[col] < 0
        ).sum()

    print(
        f"Negative Distances: {negative_distances}"
    )

    source_missing = (
        ~edge_df[
            "source_region_id"
        ].isin(
            node_df["region_id"]
        )
    ).sum()

    target_missing = (
        ~edge_df[
            "target_region_id"
        ].isin(
            node_df["region_id"]
        )
    ).sum()

    print(
        f"Invalid Edge Sources: {source_missing}"
    )

    print(
        f"Invalid Edge Targets: {target_missing}"
    )

    print()

    print(
        f"Feature Columns: "
        f"{len(node_df.columns) - 1}"
    )

    print()

    if (
        duplicate_regions == 0
        and null_values == 0
        and source_missing == 0
        and target_missing == 0
    ):
        print(
            "VALIDATION PASSED"
        )
    else:
        print(
            "VALIDATION FAILED"
        )


if __name__ == "__main__":
    main()