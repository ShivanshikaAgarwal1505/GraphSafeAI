from pathlib import Path

import networkx as nx
import pandas as pd


class NetworkXGraphBuilder:

    def build(self):

        nodes_df = pd.read_csv(
            "data/processed/osm_nodes.csv"
        )

        edges_df = pd.read_csv(
            "data/processed/osm_edges.csv"
        )

        graph = nx.Graph()

        for _, row in nodes_df.iterrows():

            graph.add_node(
                int(row["node_id"]),
                latitude=row["latitude"],
                longitude=row["longitude"]
            )

        for _, row in edges_df.iterrows():

            graph.add_edge(
                int(row["source"]),
                int(row["target"]),
                road_type=row["road_type"],
                osm_id=row["osm_id"]
            )

        return graph