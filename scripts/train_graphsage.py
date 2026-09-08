from services.graph_learning.infrastructure.trainer import (
    Trainer
)


def main():

    Trainer().train()

    print(
        "Training completed."
    )


if __name__ == "__main__":
    main()