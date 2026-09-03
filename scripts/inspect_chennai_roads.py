import geopandas as gpd


def main():

    roads = gpd.read_file(
        "data/raw/chennai_roads.geojson"
    )

    print()

    print("Columns:")

    print(roads.columns.tolist())

    print()

    print(roads.head())


if __name__ == "__main__":
    main()