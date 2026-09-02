import pandas as pd


def test():

    df = pd.read_csv(
        "data/processed/graph_embeddings.csv"
    )

    print(
        "Regions:",
        len(df)
    )

    print(
        "Dimensions:",
        len(df.columns) - 1
    )


if __name__ == "__main__":
    test()