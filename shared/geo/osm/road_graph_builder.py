from pathlib import Path

import geopandas as gpd
import pandas as pd


class RoadGraphBuilderV2:

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

            try:
                coords = list(
                    geometry.coords
                )
            except Exception:
                continue

            if len(coords) < 2:
                continue

            for i in range(
                len(coords) - 1
            ):

                start = coords[i]
                end = coords[i + 1]

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

        nodes_df = pd.DataFrame(nodes)

        edges_df = pd.DataFrame(edges)

        nodes_df.to_csv(
            output_dir / "osm_nodes_v2.csv",
            index=False
        )

        edges_df.to_csv(
            output_dir / "osm_edges_v2.csv",
            index=False
        )

        print()

        print(
            f"Nodes: {len(nodes_df)}"
        )

        print(
            f"Edges: {len(edges_df)}"
        )

        return (
            len(nodes_df),
            len(edges_df)
        )