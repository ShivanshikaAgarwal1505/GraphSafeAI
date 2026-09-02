from pathlib import Path

import pandas as pd

from services.graph_learning.embedding_extractor import (
    EmbeddingExtractor
)


def main():

    embeddings = (
        EmbeddingExtractor()
        .extract()
    )

    rows = []

    for region_id, vector in enumerate(
        embeddings.numpy(),
        start=1
    ):

        row = {
            "region_id": region_id
        }

        for i, value in enumerate(vector):

            row[
                f"embedding_{i}"
            ] = float(value)

        rows.append(row)

    df = pd.DataFrame(rows)

    output_dir = Path(
        "data/processed"
    )

    output_dir.mkdir(
        parents=True,
        exist_ok=True
    )

    output_file = (
        output_dir /
        "graph_embeddings.csv"
    )

    df.to_csv(
        output_file,
        index=False
    )

    print(
        f"Exported {len(df)} embeddings"
    )

    print(
        f"Saved: {output_file}"
    )


if __name__ == "__main__":
    main()