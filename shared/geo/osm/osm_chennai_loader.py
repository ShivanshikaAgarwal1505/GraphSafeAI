import osmnx as ox


class ChennaiOSMLoader:

    def load_graph(self):

        graph = ox.graph_from_place(
            "Chennai, Tamil Nadu, India",
            network_type="drive"
        )

        return graph