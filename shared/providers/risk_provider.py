from shared.database.models.safety_feature import (
    SafetyFeature
)


class RiskProvider:

    def get_risk_map(
        self,
        db
    ):

        rows = (
            db.query(
                SafetyFeature
            )
            .all()
        )

        return {

            row.region_id:
            row.final_risk

            for row in rows
        }