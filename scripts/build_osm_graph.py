from shared.geo.osm.road_graph_builder import (
    RoadGraphBuilder
)


def main():

    nodes, edges = (
        RoadGraphBuilder()
        .build()
    )

    print()

    print(
        f"Nodes: {nodes}"
    )

    print(
        f"Edges: {edges}"
    )


if __name__ == "__main__":
    main()