from shared.database.session import SessionLocal

from services.safety_intelligence.application.feature_builder import (
    FeatureBuilder
)


def main():

    db = SessionLocal()

    FeatureBuilder().build_features(db)

    print(
        "Region features generated."
    )

    db.close()


if __name__ == "__main__":
    main()