import geopandas as gpd
import pandas as pd

from shared.geo.osm.chennai_bbox import (
    CHENNAI_BBOX
)

from shared.geo.osm.tag_parser import (
    extract_tag
)

from shared.geo.osm.amenity_config import (
    AMENITY_TYPES
)

PBF_PATH = (
    r"C:\Users\T9978\Projects\ProjectCodes"
    r"\Railway-AI-Traffic-Optimization"
    r"\data\raw\india-latest.osm.pbf"
)


class AmenityExtractor:

    def extract(self):

        min_lon, min_lat, max_lon, max_lat = (
            CHENNAI_BBOX
        )

        points = gpd.read_file(
            PBF_PATH,
            layer="points",
            bbox=(
                min_lon,
                min_lat,
                max_lon,
                max_lat
            )
        )

        rows = []

        for _, row in points.iterrows():

            amenity = extract_tag(
                row.get(
                    "other_tags"
                ),
                "amenity"
            )

            if amenity not in (
                AMENITY_TYPES
            ):
                continue

            rows.append(
                {
                    "osm_id":
                        row["osm_id"],

                    "name":
                        row.get(
                            "name"
                        ),

                    "amenity":
                        amenity,

                    "latitude":
                        row.geometry.y,

                    "longitude":
                        row.geometry.x,
                }
            )

        return pd.DataFrame(rows)