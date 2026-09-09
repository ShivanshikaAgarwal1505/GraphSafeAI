from shared.providers.road_graph_provider import (
    RoadGraphProvider
)


class NodeRegionProvider:

    _node_to_region = None

    @classmethod
    def _build(cls):

        if cls._node_to_region is not None:
            return

        mapping = (
            RoadGraphProvider()
            .get_node_region_map()
        )

        cls._node_to_region = {

            int(row.node_id):
            int(row.region_id)

            for row in mapping.itertuples(
                index=False
            )
        }

        print(
            f"Node region map loaded: "
            f"{len(cls._node_to_region)}"
        )

    @classmethod
    def get_region(
        cls,
        node_id: int
    ):

        cls._build()

        return cls._node_to_region.get(
            node_id
        )