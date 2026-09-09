from collections import defaultdict

from services.navigation_engine.application.geo_utils import (
    GeoUtils
)

from services.navigation_engine.application.node_lookup import (
    NodeLookup
)

from services.navigation_engine.infrastructure.navigation_repository import (
    NavigationRepository
)


class GraphBuilder:

    _graph = None

    @classmethod
    def build(cls):

        if cls._graph is not None:
            return cls._graph

        repository = (
            NavigationRepository()
        )

        edges = (
            repository.edges()
        )

        graph = defaultdict(list)

        print(
            "Building weighted graph..."
        )

        for row in edges.itertuples(index=False):

            source = int(
                row.source
            )

            target = int(
                row.target
            )

            source_coords = (
                NodeLookup.get(source)
            )

            target_coords = (
                NodeLookup.get(target)
            )

            if (
                source_coords is None
                or target_coords is None
            ):
                continue

            distance = (
                GeoUtils.fast_distance_km(
                    source_coords[0],
                    source_coords[1],
                    target_coords[0],
                    target_coords[1]
                )
            )

            graph[source].append(
                (
                    target,
                    distance
                )
            )

            graph[target].append(
                (
                    source,
                    distance
                )
            )

        cls._graph = dict(
            graph
        )

        print(
            f"Road graph loaded: {len(cls._graph)} nodes"
        )

        return cls._graph