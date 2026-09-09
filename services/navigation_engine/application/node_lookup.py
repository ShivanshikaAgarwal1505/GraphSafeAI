from services.navigation_engine.infrastructure.navigation_repository import (
    NavigationRepository
)


class NodeLookup:

    _lookup = None

    @classmethod
    def _build(cls):

        if cls._lookup is not None:
            return

        nodes = (
            NavigationRepository()
            .nodes()
        )

        cls._lookup = {
            int(row.node_id): (
                float(row.latitude),
                float(row.longitude)
            )
            for row in nodes.itertuples(index=False)
        }

        print(
            f"Node lookup built: {len(cls._lookup)} nodes"
        )

    @classmethod
    def get(
        cls,
        node_id: int
    ):

        cls._build()

        return cls._lookup.get(
            node_id
        )