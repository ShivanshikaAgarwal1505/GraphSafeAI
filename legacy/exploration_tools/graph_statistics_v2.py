import networkx as nx
import pandas as pd


def main():

    nodes_df = pd.read_csv(
        "data/processed/osm_nodes_v2.csv"
    )

    edges_df = pd.read_csv(
        "data/processed/osm_edges_v2.csv"
    )

    graph = nx.Graph()

    for _, row in nodes_df.iterrows():

        graph.add_node(
            int(row["node_id"])
        )

    for _, row in edges_df.iterrows():

        graph.add_edge(
            int(row["source"]),
            int(row["target"])
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

    avg_degree = (
        sum(
            dict(
                graph.degree()
            ).values()
        )
        / graph.number_of_nodes()
    )

    print()

    print(
        "Average Degree:",
        round(avg_degree, 2)
    )


if __name__ == "__main__":
    main()