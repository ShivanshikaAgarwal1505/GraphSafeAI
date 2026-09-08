from collections import defaultdict
from datetime import datetime
from datetime import timedelta

from shared.database.models.community_report import (
    CommunityReport
)

from shared.database.models.region import (
    Region
)

from shared.database.models.region_edge import (
    RegionEdge
)

from shared.database.models.safety_feature import (
    SafetyFeature
)

import logging

logger = logging.getLogger(__name__)

class SafetyFeatureService:

    def generate_all(
        self,
        db
    ):

        db.query(
            SafetyFeature
        ).delete()

        db.commit()

        reports = (
            db.query(
                CommunityReport
            )
            .all()
        )

        regions = (
            db.query(
                Region
            )
            .all()
        )

        region_stats = defaultdict(
            lambda: {
                "report_count": 0,
                "severity_sum": 0,
                "high_severity_count": 0,
                "recent_report_count": 0,
                "categories": set(),
                "reports_last_7_days": 0,
                "reports_last_30_days": 0,
                "reports_last_90_days": 0,
            }
        )

        now = datetime.utcnow()

        cutoff_7 = now - timedelta(days=7)
        cutoff_30 = now - timedelta(days=30)
        cutoff_90 = now - timedelta(days=90)

        for report in reports:

            region_id = report.region_id

            if region_id is None:
                continue

            stats = region_stats[
                region_id
            ]

            stats["report_count"] += 1
            stats["severity_sum"] += report.severity

            stats["categories"].add(
                report.category
            )

            if report.severity >= 4:
                stats[
                    "high_severity_count"
                ] += 1

            if report.timestamp >= cutoff_30:
                stats[
                    "recent_report_count"
                ] += 1

            if report.timestamp >= cutoff_7:
                stats[
                    "reports_last_7_days"
                ] += 1

            if report.timestamp >= cutoff_30:
                stats[
                    "reports_last_30_days"
                ] += 1

            if report.timestamp >= cutoff_90:
                stats[
                    "reports_last_90_days"
                ] += 1

        edges = (
            db.query(
                RegionEdge
            )
            .filter(
                (RegionEdge.source_region_id == region_id)
                    |
                (RegionEdge.target_region_id == region_id)
            )
            .all()
        )

        degree_map = defaultdict(int)

        adjacency = defaultdict(set)

        for edge in edges:

            degree_map[
                edge.source_region_id
            ] += 1

            degree_map[
                edge.target_region_id
            ] += 1

            adjacency[
                edge.source_region_id
            ].add(
                edge.target_region_id
            )

            adjacency[
                edge.target_region_id
            ].add(
                edge.source_region_id
            )

        for region in regions:

            region_id = region.id

            stats = region_stats[
                region_id
            ]

            report_count = (
                stats["report_count"]
            )

            avg_severity = 0

            if report_count > 0:

                avg_severity = (
                    stats["severity_sum"]
                    /
                    report_count
                )

            incident_diversity = len(
                stats["categories"]
            )

            neighbor_regions = adjacency[
                region_id
            ]

            neighbor_report_count = 0
            neighbor_avg_severity = 0
            neighbor_incident_diversity = 0

            if neighbor_regions:

                report_values = []
                severity_values = []
                diversity_values = []

                for neighbor_id in neighbor_regions:

                    neighbor_stats = (
                        region_stats[
                            neighbor_id
                        ]
                    )

                    report_values.append(
                        neighbor_stats[
                            "report_count"
                        ]
                    )

                    diversity_values.append(
                        len(
                            neighbor_stats[
                                "categories"
                            ]
                        )
                    )

                    if (
                        neighbor_stats[
                            "report_count"
                        ] > 0
                    ):

                        severity_values.append(
                            neighbor_stats[
                                "severity_sum"
                            ]
                            /
                            neighbor_stats[
                                "report_count"
                            ]
                        )

                neighbor_report_count = (
                    sum(report_values)
                    /
                    len(report_values)
                )

                neighbor_incident_diversity = (
                    sum(diversity_values)
                    /
                    len(diversity_values)
                )

                if severity_values:

                    neighbor_avg_severity = (
                        sum(severity_values)
                        /
                        len(severity_values)
                    )

            safety_score = (
                (avg_severity * 0.4)
                +
                (report_count * 0.3)
                +
                (
                    stats[
                        "high_severity_count"
                    ] * 0.2
                )
                +
                (
                    stats[
                        "recent_report_count"
                    ] * 0.1
                )
            )

            incident_growth_rate = 0

            if (
                stats[
                    "reports_last_30_days"
                ] > 0
            ):

                incident_growth_rate = (
                    stats[
                        "reports_last_7_days"
                    ]
                    /
                    stats[
                        "reports_last_30_days"
                    ]
                )

            db.add(
                SafetyFeature(
                    region_id=region_id,
                    report_count=report_count,
                    avg_severity=avg_severity,
                    high_severity_count=stats[
                        "high_severity_count"
                    ],
                    recent_report_count=stats[
                        "recent_report_count"
                    ],
                    incident_diversity=incident_diversity,
                    neighbor_report_count=neighbor_report_count,
                    neighbor_avg_severity=neighbor_avg_severity,
                    neighbor_incident_diversity=neighbor_incident_diversity,
                    degree=degree_map[region_id],
                    safety_score=safety_score,
                    reports_last_7_days=stats[
                        "reports_last_7_days"
                    ],
                    reports_last_30_days=stats[
                        "reports_last_30_days"
                    ],
                    reports_last_90_days=stats[
                        "reports_last_90_days"
                    ],
                    incident_growth_rate=incident_growth_rate
                )
            )

        db.commit()

    def get_feature(
        self,
        db,
        region_id: int
    ):

        return (
            db.query(
                SafetyFeature
            )
            .filter(
                SafetyFeature.region_id
                == region_id
            )
            .first()
        )

    def generate_region(
    self,
    db,
    region_id: int
    ):

        now = datetime.utcnow()

        cutoff_7 = now - timedelta(days=7)
        cutoff_30 = now - timedelta(days=30)
        cutoff_90 = now - timedelta(days=90)

        reports = (
        db.query(
            CommunityReport
        )
        .filter(
            CommunityReport.region_id
            == region_id
        )
        .all()
        )

        report_count = len(
        reports
        )

        severity_sum = sum(
        report.severity
        for report in reports
        )

        avg_severity = (
        severity_sum / report_count
        if report_count
        else 0
        )

        high_severity_count = sum(
        1
        for report in reports
        if report.severity >= 4
        )

        categories = {
        report.category
        for report in reports
        }

        reports_last_7_days = sum(
        1
        for report in reports
        if report.timestamp >= cutoff_7
        )

        reports_last_30_days = sum(
        1
        for report in reports
        if report.timestamp >= cutoff_30
        )

        reports_last_90_days = sum(
        1
        for report in reports
        if report.timestamp >= cutoff_90
        )

        recent_report_count = (
        reports_last_30_days
        )

        incident_growth_rate = 0

        if reports_last_30_days > 0:

            incident_growth_rate = (
                reports_last_7_days
                /
                reports_last_30_days
            )

    #
    # Neighbor Metrics
    #

        edges = (
        db.query(
            RegionEdge
        )
        .all()
        )

        neighbor_ids = set()

        for edge in edges:

            if edge.source_region_id == region_id:

                neighbor_ids.add(
                edge.target_region_id
                )

            elif edge.target_region_id == region_id:

                neighbor_ids.add(
                edge.source_region_id
                )

        degree = len(
        neighbor_ids
        )

        neighbor_report_count = 0
        neighbor_avg_severity = 0
        neighbor_incident_diversity = 0

        if neighbor_ids:

            report_values = []
            severity_values = []
            diversity_values = []

            for neighbor_id in neighbor_ids:

                neighbor_reports = (
                db.query(
                    CommunityReport
                )
                .filter(
                    CommunityReport.region_id
                    == neighbor_id
                )
                .all()
                )

                report_values.append(
                len(
                    neighbor_reports
                )
                )

                diversity_values.append(
                len(
                    {
                        report.category
                        for report
                        in neighbor_reports
                    }
                )
                )

                if neighbor_reports:

                    severity_values.append(
                    sum(
                        report.severity
                        for report
                        in neighbor_reports
                    )
                    /
                    len(
                        neighbor_reports
                    )
                    )

            neighbor_report_count = (
            sum(report_values)
            /
            len(report_values)
            )

            neighbor_incident_diversity = (
            sum(diversity_values)
            /
            len(diversity_values)
            )

            if severity_values:

                neighbor_avg_severity = (
                sum(severity_values)
                /
                len(severity_values)
                )

    #
    # Safety Score
    #

        safety_score = (

        (avg_severity * 0.4)

        +

        (report_count * 0.3)

        +

        (
            high_severity_count
            * 0.2
        )

        +

        (
            recent_report_count
            * 0.1
        )
        )

        feature = self.get_feature(
        db,
        region_id
        )

        if not feature:

            feature = SafetyFeature(
            region_id=region_id
            )

            db.add(
            feature
            )

        feature.report_count = (
        report_count
        )

        feature.avg_severity = (
        avg_severity
        )

        feature.high_severity_count = (
        high_severity_count
        )

        feature.recent_report_count = (
            recent_report_count
        )

        feature.incident_diversity = (
        len(categories)
        )

        feature.reports_last_7_days = (
        reports_last_7_days
        )

        feature.reports_last_30_days = (
        reports_last_30_days
        )

        feature.reports_last_90_days = (
        reports_last_90_days
        )

        feature.incident_growth_rate = (
        incident_growth_rate
        )

        feature.neighbor_report_count = (
        neighbor_report_count
        )

        feature.neighbor_avg_severity = (
        neighbor_avg_severity
        )

        feature.neighbor_incident_diversity = (
        neighbor_incident_diversity
        )

        feature.degree = (
        degree
        )

        feature.safety_score = (
        safety_score
        )

        logger.info(
        "[FEATURES] region=%s reports=%s severity=%.2f neighbors=%s",
        region_id,
        report_count,
        avg_severity,
        degree
        )

        db.flush()