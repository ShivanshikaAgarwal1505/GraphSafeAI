import torch

from torch.nn import Linear

from torch_geometric.nn import SAGEConv


class GraphSAGEModel(
    torch.nn.Module
):

    def __init__(
        self,
        in_channels,
        hidden_channels=16
    ):
        super().__init__()

        self.conv1 = SAGEConv(
            in_channels,
            hidden_channels
        )

        self.conv2 = SAGEConv(
            hidden_channels,
            hidden_channels
        )

        self.head = Linear(
            hidden_channels,
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