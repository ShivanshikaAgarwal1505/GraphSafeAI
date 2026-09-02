import torch

from services.graph_learning.trainer import (
    Trainer
)


def main():

    model = (
        Trainer()
        .train()
    )

    torch.save(
        model.state_dict(),
        "models/graphsage/model.pt"
    )

    print(
        "Model saved."
    )


if __name__ == "__main__":
    main()