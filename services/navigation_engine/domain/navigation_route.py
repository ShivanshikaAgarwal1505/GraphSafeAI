from dataclasses import dataclass


@dataclass
class NavigationRoute:

    source_node: int

    destination_node: int

    route_nodes: list[int]