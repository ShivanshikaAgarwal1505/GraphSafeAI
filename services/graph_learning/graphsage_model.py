import torch

from torch.nn import Linear

from torch_geometric.nn import SAGEConv


class GraphSAGEModel(
    torch.nn.Module
):

    def __init__(self):

        super().__init__()

        self.conv1 = SAGEConv(
            5,
            16
        )

        self.conv2 = SAGEConv(
            16,
            16
        )

        self.head = Linear(
            16,
            1
        )

    def forward(
        self,
        x,
        edge_index
    ):

        x = self.conv1(
            x,
            edge_index
        )

        x = torch.relu(x)

        x = self.conv2(
            x,
            edge_index
        )

        x = torch.relu(x)

        out = self.head(x)

        return out.squeeze()