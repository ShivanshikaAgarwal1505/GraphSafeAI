from services.graph_learning.dataset_builder import (
    DatasetBuilder,
)


def test_dataset():

    data = (
        DatasetBuilder()
        .build()
    )

    print(data)
    print()

    print("Nodes:", data.num_nodes)

    print(
        "Features:",
        data.num_features
    )

    print(
        "Edges:",
        data.edge_index.shape[1]
    )


if __name__ == "__main__":
    test_dataset()