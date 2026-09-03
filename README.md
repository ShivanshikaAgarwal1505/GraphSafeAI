# GraphSafeAI v2

GraphSafeAI is a graph-based urban safety intelligence platform that uses OpenStreetMap road networks and Graph Neural Networks (GraphSAGE) to model spatial safety patterns.

## Current Architecture

### Region Generation

The system derives spatial regions from OpenStreetMap road-network nodes using geographic grid aggregation.

### Data Pipeline

OpenStreetMap Road Network
→ Region Generation
→ Region Edge Generation
→ Node Feature Generation
→ Region Database
→ Graph Dataset Export
→ GraphSAGE Training
→ Embedding Generation
→ Clustering
→ Hotspot Detection

### Current Scale

- Road Nodes: ~439,067
- Road Edges: ~486,343
- Regions: 4,934
- Region Edges: 12,897

### Migration Status

The project has completed migration from the legacy synthetic grid-based graph:

Legacy:
- 231 regions
- 430 edges

Current:
- 4,934 OSM-derived regions
- 12,897 region edges

All graph learning and hotspot detection workflows now operate on OSM-derived spatial data.

## Active Pipeline

```text
python -m scripts.load_chennai_osm

python -m scripts.build_osm_graph

python -m scripts.generate_regions

python -m scripts.generate_region_edges

python -m scripts.generate_node_features

python -m scripts.load_regions

python -m scripts.build_region_graph

python -m scripts.load_safety_features

python -m scripts.export_graph_dataset

python -m scripts.train_graphsage

python -m scripts.export_embeddings

python -m scripts.cluster_regions

python -m scripts.detect_hotspots

```