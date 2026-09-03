from pathlib import Path

import geopandas as gpd
import pandas as pd


class RoadGraphBuilder:

    def build(self):

        roads = gpd.read_file(
            "data/raw/chennai_roads.geojson"
        )

        node_lookup = {}

        nodes = []
        edges = []

        next_node_id = 1

        for _, road in roads.iterrows():

            geometry = road.geometry

            if geometry is None:
                continue

            coords = list(
                geometry.coords
            )

            if len(coords) < 2:
                continue

            start = coords[0]
            end = coords[-1]

            if start not in node_lookup:

                node_lookup[start] = (
                    next_node_id
                )

                nodes.append(
                    {
                        "node_id":
                            next_node_id,
                        "longitude":
                            start[0],
                        "latitude":
                            start[1]
                    }
                )

                next_node_id += 1

            if end not in node_lookup:

                node_lookup[end] = (
                    next_node_id
                )

                nodes.append(
                    {
                        "node_id":
                            next_node_id,
                        "longitude":
                            end[0],
                        "latitude":
                            end[1]
                    }
                )

                next_node_id += 1

            edges.append(
                {
                    "source":
                        node_lookup[start],
                    "target":
                        node_lookup[end],
                    "osm_id":
                        road.osm_id,
                    "road_type":
                        road.highway
                }
            )

        output_dir = Path(
            "data/processed"
        )

        output_dir.mkdir(
            parents=True,
            exist_ok=True
        )

        pd.DataFrame(nodes).to_csv(
            output_dir /
            "osm_nodes.csv",
            index=False
        )

        pd.DataFrame(edges).to_csv(
            output_dir /
            "osm_edges.csv",
            index=False
        )

        return (
            len(nodes),
            len(edges)
        )