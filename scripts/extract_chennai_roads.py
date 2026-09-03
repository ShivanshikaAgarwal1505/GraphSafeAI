from pathlib import Path

import geopandas as gpd

from shared.geo.osm.chennai_bbox import (
    CHENNAI_BBOX
)

PBF_PATH = (
    r"C:\Users\T9978\Projects\ProjectCodes"
    r"\Railway-AI-Traffic-Optimization"
    r"\data\raw\india-latest.osm.pbf"
)


def main():

    min_lon, min_lat, max_lon, max_lat = (
        CHENNAI_BBOX
    )

    print(
        "Reading OSM roads..."
    )

    roads = gpd.read_file(
        PBF_PATH,
        layer="lines",
        bbox=(
            min_lon,
            min_lat,
            max_lon,
            max_lat
        )
    )

    print()

    print(
        f"Road records: {len(roads)}"
    )

    output_dir = Path(
        "data/raw"
    )

    output_dir.mkdir(
        parents=True,
        exist_ok=True
    )

    output_file = (
        output_dir /
        "chennai_roads.geojson"
    )

    roads.to_file(
        output_file,
        driver="GeoJSON"
    )

    print(
        f"Saved: {output_file}"
    )


if __name__ == "__main__":
    main()