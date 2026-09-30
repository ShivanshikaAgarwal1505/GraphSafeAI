from scipy.spatial import cKDTree
import geopandas as gpd

from shared.database.session import SessionLocal
from shared.database.models.region import Region
from shared.geo.osm.chennai_bbox import CHENNAI_BBOX

PBF_PATH = (
    r"C:\Users\T9978\Projects\ProjectCodes"
    r"\Railway-AI-Traffic-Optimization"
    r"\data\raw\india-latest.osm.pbf"
)

def load_places():

    min_lon, min_lat, max_lon, max_lat = (
        CHENNAI_BBOX
    )

    print("Loading Chennai places...")

    points = gpd.read_file(
        PBF_PATH,
        layer="points",
        bbox=(
            min_lon,
            min_lat,
            max_lon,
            max_lat,
        ),
    )

    places = points[
        points["place"].isin(
            [
                "neighbourhood",
                "suburb",
                "locality",
                "town",
                "city",
                "quarter",
            ]
        )
    ].copy()

    places = places[
        places["name"].notna()
    ]

    places = places.drop_duplicates(
        subset=["name"]
    )

    print(
        f"Found {len(places)} locality names"
    )

    return places


def update_region_names():

    db = SessionLocal()

    places = load_places()

    tree = cKDTree(
        list(
            zip(
                places.geometry.y,
                places.geometry.x,
            )
        )
    )

    regions = (
        db.query(Region)
        .all()
    )

    print(
        f"Updating {len(regions)} regions..."
    )

    updated = 0

    for region in regions:

        _, idx = tree.query(
            [
                region.centroid_lat,
                region.centroid_lon,
            ]
        )

        region.region_name = (
            str(
                places.iloc[idx]["name"]
            )
        )

        updated += 1

        if updated % 500 == 0:
            print(
                f"Updated {updated} regions..."
            )

    db.commit()

    print()
    print(
        f"Successfully updated {updated} regions"
    )

    db.close()


if __name__ == "__main__":
    update_region_names()