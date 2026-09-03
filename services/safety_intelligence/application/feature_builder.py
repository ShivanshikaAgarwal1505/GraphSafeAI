from collections import defaultdict

from shared.database.models.community_report import (
    CommunityReport,
)

from shared.database.models.region import (
    Region,
)

from shared.database.models.region_edge import (
    RegionEdge,
)

from shared.database.models.safety_feature import (
    SafetyFeature,
)

from GraphSafeAIv2.shared.geo.region_mapper import (
    RegionMapper,
)


class FeatureBuilder:

    def build_features(self, db):

        db.query(
            SafetyFeature
        ).delete()

        db.commit()

        regions = (
            db.query(
                Region
            ).all()
        )

        reports = (
            db.query(
                CommunityReport
            ).all()
        )

        edges = (
            db.query(
                RegionEdge
            ).all()
        )

        # ----------------------------------
        # Build adjacency map
        # ----------------------------------

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

        # ----------------------------------
        # Assign reports to regions
        # ----------------------------------

        mapper = RegionMapper()

        reports_by_region = defaultdict(list)

        for report in reports:

            region_id = (
                mapper.find_region(
                    report.latitude,
                    report.longitude
                )
            )

            if region_id is not None:

                reports_by_region[
                    region_id
                ].append(
                    report
                )

        # ----------------------------------
        # Build region metrics
        # ----------------------------------

        region_metrics = {}

        for region in regions:

            assigned_reports = (
                reports_by_region.get(
                    region.id,
                    []
                )
            )

            report_count = len(
                assigned_reports
            )

            avg_severity = (
                sum(
                    report.severity
                    for report in assigned_reports
                )
                / report_count
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

        # ----------------------------------
        # Generate graph-aware features
        # ----------------------------------

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

            neighbors = (
                neighbor_map.get(
                    region.id,
                    []
                )
            )

            degree = len(
                neighbors
            )

            if degree > 0:

                neighbor_report_count = (
                    sum(
                        region_metrics[n][
                            "report_count"
                        ]
                        for n in neighbors
                    )
                    / degree
                )

                neighbor_avg_severity = (
                    sum(
                        region_metrics[n][
                            "avg_severity"
                        ]
                        for n in neighbors
                    )
                    / degree
                )

            else:

                neighbor_report_count = 0

                neighbor_avg_severity = 0

            safety_score = max(
                0.0,
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

        print(
            f"Generated safety features for {len(regions)} regions"
        )