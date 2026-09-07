from subprocess import run


class RiskRefreshService:

    def refresh(self):

        run(
            [
                "python",
                "-m",
                "scripts.generate_safety_features"
            ],
            check=True
        )

        run(
            [
                "python",
                "-m",
                "scripts.generate_risk_scores"
            ],
            check=True
        )
