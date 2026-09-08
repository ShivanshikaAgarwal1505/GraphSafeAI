from shared.database.session import (
    SessionLocal
)

from services.safety_intelligence.application.risk_score_service import (
    RiskScoreService
)


def main():

    db = SessionLocal()

    service = RiskScoreService()

    service.calculate_all(
        db
    )

    db.close()


if __name__ == "__main__":
    main()