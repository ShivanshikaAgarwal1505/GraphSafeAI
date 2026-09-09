from collections import defaultdict
from collections import deque

from shared.database.session import SessionLocal

from shared.database.models.region import (
    Region
)

from shared.database.models.region_edge import (
    RegionEdge
)


def main():

    db = SessionLocal()

    adjacency = defaultdict(list)

    edges = (
        db.query(
            RegionEdge
        )
        .all()
    )

    for edge in edges:

        adjacency[
            edge.source_region_id
        ].append(
            edge.target_region_id
        )

        adjacency[
            edge.target_region_id
        ].append(
            edge.source_region_id
        )

    regions = {

        region.id

        for region in (
            db.query(
                Region
            )
            .all()
        )
    }

    total_regions = len(
        regions
    )

    total_edges = len(
        edges
    )

    degrees = [

        len(
            adjacency[
                region
            ]
        )

        for region in regions
    ]

    connected_components = []

    visited = set()

    for region in regions:

        if region in visited:
            continue

        queue = deque(
            [region]
        )

        component = []

        while queue:

            current = (
                queue.popleft()
            )

            if current in visited:
                continue

            visited.add(
                current
            )

            component.append(
                current
            )

            for neighbor in adjacency[
                current
            ]:

                if neighbor not in visited:

                    queue.append(
                        neighbor
                    )

        connected_components.append(
            component
        )

    largest_component = max(
        connected_components,
        key=len
    )

    isolated_regions = [

        region

        for region in regions

        if len(
            adjacency[
                region
            ]
        ) == 0
    ]

    print()

    print(
        "========== GRAPH ANALYSIS =========="
    )

    print(
        f"Total Regions       : {total_regions}"
    )

    print(
        f"Total Edges         : {total_edges}"
    )

    print(
        f"Connected Components: {len(connected_components)}"
    )

    print(
        f"Largest Component   : {len(largest_component)}"
    )

    print(
        f"Average Degree      : {sum(degrees)/len(degrees):.2f}"
    )

    print(
        f"Max Degree          : {max(degrees)}"
    )

    print(
        f"Min Degree          : {min(degrees)}"
    )

    print(
        f"Isolated Regions    : {len(isolated_regions)}"
    )

    print(
        "===================================="
    )

    print()

    largest = sorted(
        connected_components,
        key=len,
        reverse=True
    )

    print(
        "Top 10 Components"
    )

    for index, component in enumerate(
        largest[:10],
        start=1
    ):

        print(
            f"{index}. {len(component)}"
        )


if __name__ == "__main__":
    main()