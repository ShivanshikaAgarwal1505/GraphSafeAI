from collections import defaultdict
from datetime import datetime
from datetime import timedelta

# from GraphSafeAIv2.services.community_reporting.domain import report
from shared.database.session import SessionLocal

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

from shared.geo.region_mapper import (
    RegionMapper
)

def main():

    db = SessionLocal()

    db.query(
        SafetyFeature
    ).delete()

    db.commit()

    mapper = RegionMapper()

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

    #
    # Build region stats
    #

    for report in reports:

        region_id = (
            mapper.find_region(
                latitude=report.latitude,
                longitude=report.longitude
            )
        )

        if region_id is None:
            continue

        stats = region_stats[
            region_id
        ]

        stats[
            "report_count"
        ] += 1

        stats[
            "severity_sum"
        ] += report.severity

        stats[
            "categories"
        ].add(
            report.category
        )

        if report.severity >= 4:

            stats[
                "high_severity_count"
            ] += 1

        if report.timestamp >= cutoff_30:
            stats["recent_report_count"] += 1

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

    #
    # Load graph edges
    #

    edges = (
        db.query(
            RegionEdge
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

    #
    # Create features
    #

    inserted = 0

    for region in regions:

        region_id = region.id

        stats = region_stats[
            region_id
        ]

        report_count = (
            stats[
                "report_count"
            ]
        )

        avg_severity = 0

        if report_count > 0:

            avg_severity = (
                stats[
                    "severity_sum"
                ]
                /
                report_count
            )

        incident_diversity = len(
            stats[
                "categories"
            ]
        )

        #
        # Neighbor statistics
        #

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

                neighbor_stats = region_stats[
                    neighbor_id
                ]

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

                high_severity_count=(
                    stats[
                        "high_severity_count"
                    ]
                ),

                recent_report_count=(
                    stats[
                        "recent_report_count"
                    ]
                ),

                incident_diversity=(
                    incident_diversity
                ),

                neighbor_report_count=(
                    neighbor_report_count
                ),

                neighbor_avg_severity=(
                    neighbor_avg_severity
                ),

                neighbor_incident_diversity=(
                    neighbor_incident_diversity
                ),

                degree=degree_map[
                    region_id
                ],

                safety_score=safety_score,

                reports_last_7_days=(
                    stats[
                        "reports_last_7_days"
                    ]
                ),

                reports_last_30_days=(
                    stats[
                        "reports_last_30_days"
                    ]
                ),

                reports_last_90_days=(
                    stats[
                        "reports_last_90_days"
                    ]
                ),

                incident_growth_rate=(
                    incident_growth_rate
                ),
            )
        )

        inserted += 1

    db.commit()

    print()
    print(f"Reports: {len(reports)}")
    print(f"Regions: {len(regions)}")
    print(f"Features Generated: {inserted}")

    db.close()


if __name__ == "__main__":
    main()