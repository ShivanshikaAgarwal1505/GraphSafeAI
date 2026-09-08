# GraphSafeAI v2

GraphSafeAI is a graph-based urban safety intelligence platform that combines OpenStreetMap infrastructure data, community-reported safety incidents, graph intelligence, and Graph Neural Networks (GraphSAGE) to model, analyze, and predict urban safety patterns.

The platform evolves from infrastructure-driven safety assessment toward evidence-driven risk intelligence as real-world incident reports accumulate over time.

---

# Vision

GraphSafeAI aims to answer:

- Which regions are structurally vulnerable?
- Which areas are becoming less safe over time?
- How does risk propagate through neighboring regions?
- What safety patterns emerge from community reports?
- How can urban safety be continuously monitored, predicted, and improved?

---

# System Architecture

```text
Community Reports
        +
OpenStreetMap Infrastructure
        +
Region Connectivity Graph
                ↓

        Safety Intelligence
                ↓

        Risk Intelligence
                ↓

        Feature Registry
                ↓

        Dataset Builder
                ↓

    PyTorch Geometric Dataset
                ↓

        GraphSAGE Model
                ↓

            Evaluator
    (RMSE / MAE / R²)
                ↓

            MLflow
    Experiment Tracking
                ↓

        Model Registry
                ↓

            Predictor
                ↓

        Predictions DB
                ↓

        Prediction APIs
```

---

# Development Status

## Phase 1 - Spatial Intelligence

Completed ✅

## Phase 2 - Safety Intelligence

Completed ✅

## Phase 3 - Graph Learning

Completed ✅

- Feature Registry
- Dynamic Dataset Builder
- GraphSAGE Training
- Evaluator
- MLflow Integration
- Model Registry
- Predictor
- Prediction Service
- Prediction APIs
- Prediction Persistence

---

# Roadmap

## Phase 4

- Routing Engine
- Emergency Response Engine
- GraphRAG Engine

## Future Enhancements
- Safe Route Recommendation
- Explainable Predictions
- Real-Time Prediction Updates
- City Intelligence Dashboard
- Public Safety APIs
- Decision Support Systems