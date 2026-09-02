from shared.database.models.region import Region
from shared.database.models.community_report import CommunityReport
from shared.database.models.safety_feature import SafetyFeature

from shared.geo.spatial_utils import (
    euclidean_distance
)


class FeatureBuilder:

    def build_features(
        self,
        db
    ):

        db.query(
            SafetyFeature
        ).delete()

        db.commit()

        regions = (
            db.query(Region)
            .all()
        )

        reports = (
            db.query(CommunityReport)
            .all()
        )

        for region in regions:

            assigned = []

            for report in reports:

                distance = euclidean_distance(
                    region.centroid_lat,
                    region.centroid_lon,
                    report.latitude,
                    report.longitude
                )

                if distance < 0.02:

                    assigned.append(report)

            report_count = len(assigned)

            avg_severity = (
                sum(
                    r.severity
                    for r in assigned
                ) / report_count
                if report_count > 0
                else 0
            )

            safety_score = max(
                0,
                1 - (
                    report_count * 0.05 +
                    avg_severity * 0.1
                )
            )

            db.add(
                SafetyFeature(
                    region_id=region.id,
                    report_count=report_count,
                    avg_severity=avg_severity,
                    safety_score=safety_score
                )
            )

        db.commit()