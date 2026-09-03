import pandas as pd


def main():

    nodes = pd.read_csv(
        "data/processed/osm_nodes.csv"
    )

    edges = pd.read_csv(
        "data/processed/osm_edges.csv"
    )

    print()

    print(
        "Nodes:",
        len(nodes)
    )

    print(
        "Edges:",
        len(edges)
    )

    print()

    print(nodes.head())

    print()

    print(edges.head())


if __name__ == "__main__":
    main()