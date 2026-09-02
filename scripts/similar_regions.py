import pandas as pd

from sklearn.metrics.pairwise import (
    euclidean_distances
)


TARGET_REGION = 141


def main():

    df = pd.read_csv(
        "data/processed/graph_embeddings.csv"
    )

    target_row = df[
        df["region_id"] == TARGET_REGION
    ]

    feature_cols = [
        c
        for c in df.columns
        if c.startswith("embedding_")
    ]

    target_embedding = (
        target_row[
            feature_cols
        ].values
    )

    distances = euclidean_distances(
        target_embedding,
        df[feature_cols].values
    )[0]

    results = pd.DataFrame(
        {
            "region_id":
                df["region_id"],
            "distance":
                distances
        }
    )

    results = (
        results.sort_values(
            "distance"
        )
        .head(10)
    )

    print(
        f"Most similar regions to {TARGET_REGION}"
    )

    print(results)


if __name__ == "__main__":
    main()