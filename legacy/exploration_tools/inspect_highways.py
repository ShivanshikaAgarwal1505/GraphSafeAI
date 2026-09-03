import geopandas as gpd


def main():

    roads = gpd.read_file(
        "data/raw/chennai_roads.geojson"
    )

    print()

    print(
        roads["highway"]
        .value_counts()
        .head(30)
    )


if __name__ == "__main__":
    main()