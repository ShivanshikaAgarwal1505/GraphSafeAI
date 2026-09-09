from shared.providers.road_graph_provider import (
    RoadGraphProvider
)


class NavigationRepository:

    def __init__(
        self
    ):

        self.provider = (
            RoadGraphProvider()
        )

    def nodes(
        self
    ):

        return (
            self.provider
            .get_nodes()
        )

    def edges(
        self
    ):

        return (
            self.provider
            .get_edges()
        )

    def node_region_map(
        self
    ):

        return (
            self.provider
            .get_node_region_map()
        )