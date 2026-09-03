import networkx as nx

from shared.geo.osm.networkx_graph_builder import (
    NetworkXGraphBuilder
)


def main():

    graph = (
        NetworkXGraphBuilder()
        .build()
    )

    print()

    print(
        "Nodes:",
        graph.number_of_nodes()
    )

    print(
        "Edges:",
        graph.number_of_edges()
    )

    print()

    print(
        "Connected Components:",
        nx.number_connected_components(
            graph
        )
    )

    largest_component = max(
        nx.connected_components(graph),
        key=len
    )

    print()

    print(
        "Largest Component:",
        len(largest_component)
    )

    print()

    print(
        "Average Degree:",
        round(
            sum(
                dict(
                    graph.degree()
                ).values()
            )
            / graph.number_of_nodes(),
            2
        )
    )


if __name__ == "__main__":
    main()