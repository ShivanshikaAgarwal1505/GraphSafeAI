from collections import defaultdict
from collections import deque

from shared.database.session import SessionLocal
from shared.database.models.region import Region
from shared.database.models.region_edge import RegionEdge

db = SessionLocal()

adj = defaultdict(list)

for edge in db.query(RegionEdge).all():

    adj[edge.source_region_id].append(
        edge.target_region_id
    )

    adj[edge.target_region_id].append(
        edge.source_region_id
    )

regions = {
    region.id
    for region in db.query(Region).all()
}

visited = set()

components = []

for region in regions:

    if region in visited:
        continue

    queue = deque([region])

    component = []

    while queue:

        current = queue.popleft()

        if current in visited:
            continue

        visited.add(current)

        component.append(current)

        for neighbor in adj[current]:
            if neighbor not in visited:

                queue.append(neighbor)

    components.append(component)

print(
    f"Connected Components: {len(components)}"
)

print(
    f"Largest Component Size: {max(len(c) for c in components)}"
)