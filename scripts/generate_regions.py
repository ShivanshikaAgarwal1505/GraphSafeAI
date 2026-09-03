from pathlib import Path

import pandas as pd


NODES_FILE = "data/processed/osm_nodes_v2.csv"


def main():

    nodes = pd.read_csv(NODES_FILE)

    GRID_SIZE = 0.005

    nodes["grid_x"] = (
        nodes["longitude"] // GRID_SIZE
    ).astype(int)

    nodes["grid_y"] = (
        nodes["latitude"] // GRID_SIZE
    ).astype(int)

    grouped = nodes.groupby(
        ["grid_x", "grid_y"]
    )

    regions = []

    node_region_map = []

    region_id = 1

    for (gx, gy), group in grouped:

        center_lon = (
            group["longitude"]
            .mean()
        )

        center_lat = (
            group["latitude"]
            .mean()
        )

        regions.append(
            {
                "region_id": region_id,
                "grid_x": gx,
                "grid_y": gy,
                "center_lat": center_lat,
                "center_lon": center_lon,
                "node_count": len(group)
            }
        )

        for node_id in group["node_id"]:

            node_region_map.append(
                {
                    "node_id": node_id,
                    "region_id": region_id
                }
            )

        region_id += 1

    output_dir = Path(
        "data/processed"
    )

    pd.DataFrame(
        regions
    ).to_csv(
        output_dir / "regions.csv",
        index=False
    )

    pd.DataFrame(
        node_region_map
    ).to_csv(
        output_dir / "node_region_map.csv",
        index=False
    )

    print(
        f"Regions: {len(regions)}"
    )


if __name__ == "__main__":
    main()