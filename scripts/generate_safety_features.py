from shared.database.session import (
    SessionLocal
)

from services.safety_intelligence.application.safety_feature_service import (
    SafetyFeatureService
)


def main():

    db = SessionLocal()

    service = (
        SafetyFeatureService()
    )

    service.generate_all(
        db
    )

    db.close()


if __name__ == "__main__":
    main()