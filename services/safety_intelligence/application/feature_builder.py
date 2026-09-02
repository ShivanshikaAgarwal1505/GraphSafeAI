from collections import defaultdict

from shared.database.models.community_report import (
    CommunityReport,
)
from shared.database.models.region import Region
from shared.database.models.region_edge import (
    RegionEdge,
)
from shared.database.models.safety_feature import (
    SafetyFeature,
)

from shared.geo.spatial_utils import (
    euclidean_distance,
)


class FeatureBuilder:

    def build_features(self, db):

        # Clear old features

        db.query(SafetyFeature).delete()
        db.commit()

        # Load graph data

        regions = db.query(Region).all()

        reports = db.query(
            CommunityReport
        ).all()

        edges = db.query(
            RegionEdge
        ).all()

        # Build adjacency map

        neighbor_map = defaultdict(list)

        for edge in edges:

            neighbor_map[
                edge.source_region_id
            ].append(
                edge.target_region_id
            )

            neighbor_map[
                edge.target_region_id
            ].append(
                edge.source_region_id
            )

        # Cache region report metrics

        region_metrics = {}

        for region in regions:

            assigned_reports = []

            for report in reports:

                distance = euclidean_distance(
                    region.centroid_lat,
                    region.centroid_lon,
                    report.latitude,
                    report.longitude
                )

                if distance < 0.02:
                    assigned_reports.append(
                        report
                    )

            report_count = len(
                assigned_reports
            )

            avg_severity = (
                sum(
                    r.severity
                    for r in assigned_reports
                ) / report_count
                if report_count > 0
                else 0
            )

            region_metrics[
                region.id
            ] = {
                "report_count":
                    report_count,
                "avg_severity":
                    avg_severity
            }

        # Build graph-aware features

        for region in regions:

            report_count = (
                region_metrics[
                    region.id
                ]["report_count"]
            )

            avg_severity = (
                region_metrics[
                    region.id
                ]["avg_severity"]
            )

            neighbors = neighbor_map[
                region.id
            ]

            degree = len(
                neighbors
            )

            # Neighbor aggregates

            if degree > 0:

                neighbor_report_count = (
                    sum(
                        region_metrics[
                            n
                        ]["report_count"]
                        for n in neighbors
                    )
                    / degree
                )

                neighbor_avg_severity = (
                    sum(
                        region_metrics[
                            n
                        ]["avg_severity"]
                        for n in neighbors
                    )
                    / degree
                )

            else:

                neighbor_report_count = 0

                neighbor_avg_severity = 0

            # Graph-aware safety score

            safety_score = max(
                0,
                1 - (
                    report_count * 0.05
                    + avg_severity * 0.10
                    + neighbor_report_count * 0.03
                    + neighbor_avg_severity * 0.05
                )
            )

            db.add(
                SafetyFeature(
                    region_id=region.id,
                    report_count=report_count,
                    avg_severity=avg_severity,
                    neighbor_report_count=
                        neighbor_report_count,
                    neighbor_avg_severity=
                        neighbor_avg_severity,
                    degree=degree,
                    safety_score=safety_score
                )
            )

        db.commit()