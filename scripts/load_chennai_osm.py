from shared.geo.osm.osm_chennai_loader import (
    ChennaiOSMLoader
)


def main():

    graph = (
        ChennaiOSMLoader()
        .load_graph()
    )

    print()

    print(
        f"Nodes: {graph.number_of_nodes()}"
    )

    print(
        f"Edges: {graph.number_of_edges()}"
    )


if __name__ == "__main__":
    main()