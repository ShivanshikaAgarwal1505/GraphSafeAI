from pathlib import Path

import pandas as pd


def main():

    regions = pd.read_csv(
        "data/processed/regions.csv"
    )

    edges = []

    for _, source in regions.iterrows():

        for _, target in regions.iterrows():

            if (
                source["region_id"]
                >= target["region_id"]
            ):
                continue

            lat_diff = abs(
                source["center_lat"]
                - target["center_lat"]
            )

            lon_diff = abs(
                source["center_lon"]
                - target["center_lon"]
            )

            if (
                lat_diff <= 0.006
                and lon_diff <= 0.006
            ):

                edges.append(
                    {
                        "source":
                            source["region_id"],
                        "target":
                            target["region_id"]
                    }
                )

    pd.DataFrame(edges).to_csv(
        "data/processed/edge_list.csv",
        index=False
    )

    print(
        f"Edges: {len(edges)}"
    )


if __name__ == "__main__":
    main()