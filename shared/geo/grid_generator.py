from dataclasses import dataclass


@dataclass
class GridRegion:
    region_name: str
    centroid_lat: float
    centroid_lon: float


class ChennaiGridGenerator:

    def generate(self):

        # Chennai bounding box

        min_lat = 12.85
        max_lat = 13.25

        min_lon = 80.10
        max_lon = 80.35

        rows = 11
        cols = 21

        lat_step = (max_lat - min_lat) / rows
        lon_step = (max_lon - min_lon) / cols

        regions = []

        counter = 1

        for row in range(rows):

            for col in range(cols):

                center_lat = (
                    min_lat +
                    row * lat_step +
                    lat_step / 2
                )

                center_lon = (
                    min_lon +
                    col * lon_step +
                    lon_step / 2
                )

                regions.append(
                    GridRegion(
                        region_name=f"R{counter}",
                        centroid_lat=center_lat,
                        centroid_lon=center_lon
                    )
                )

                counter += 1

        return regions