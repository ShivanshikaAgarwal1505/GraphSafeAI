import pandas as pd


def main():

    df = pd.read_csv(
        "data/processed/node_features.csv"
    )

    hotspots = df[
        df["safety_score"] < 0.5
    ]

    hotspots = hotspots.sort_values(
        "safety_score"
    )

    hotspots.to_csv(
        "data/processed/hotspots.csv",
        index=False
    )

    print(
        f"Detected {len(hotspots)} hotspots"
    )

    print(
        hotspots[
            [
                "region_id",
                "safety_score"
            ]
        ].head(10)
    )


if __name__ == "__main__":
    main()