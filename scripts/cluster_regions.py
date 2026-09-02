from pathlib import Path

import pandas as pd

from sklearn.cluster import KMeans


def main():

    embeddings = pd.read_csv(
        "data/processed/graph_embeddings.csv"
    )

    X = embeddings.drop(
        columns=["region_id"]
    )

    kmeans = KMeans(
        n_clusters=5,
        random_state=42,
        n_init=10
    )

    embeddings["cluster_id"] = (
        kmeans.fit_predict(X)
    )

    output = Path(
        "data/processed/clustered_regions.csv"
    )

    embeddings.to_csv(
        output,
        index=False
    )

    print(
        f"Clustered {len(embeddings)} regions"
    )

    print(
        f"Saved: {output}"
    )


if __name__ == "__main__":
    main()