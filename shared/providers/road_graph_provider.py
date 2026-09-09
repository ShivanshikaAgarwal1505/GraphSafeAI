from pathlib import Path

import pandas as pd


class RoadGraphProvider:

    _instance = None

    def __new__(
        cls
    ):

        if cls._instance is None:

            cls._instance = super().__new__(
                cls
            )

            cls._instance._loaded = False

        return cls._instance

    def _load_graph(
        self
    ):

        if self._loaded:

            return

        base_path = Path(
            "data/processed"
        )

        self.nodes = pd.read_csv(
            base_path /
            "osm_nodes_v2.csv"
        )

        self.edges = pd.read_csv(
            base_path /
            "osm_edges_v2.csv"
        )

        self.node_region_map = pd.read_csv(
            base_path /
            "node_region_map.csv"
        )
        print("Loading graph...")
        self._loaded = True

    def get_nodes(
        self
    ):

        self._load_graph()

        return self.nodes

    def get_edges(
        self
    ):

        self._load_graph()

        return self.edges

    def get_node_region_map(
        self
    ):

        self._load_graph()

        return self.node_region_map