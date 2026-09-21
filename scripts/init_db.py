from shared.database.database import engine

from shared.database.models.base import Base

from shared.database.models.region import Region
from shared.database.models.community_report import (
    CommunityReport
)
from shared.database.models.region_edge import (
    RegionEdge
)
from shared.database.models.safety_feature import (
    SafetyFeature
)
from shared.database.models.prediction import (
    Prediction
)

from shared.database.models.user import User

from shared.database.models.favorite_location import (
    FavoriteLocation
)

from shared.database.models.report_vote import (
    ReportVote
)

def create_tables():

    Base.metadata.create_all(
        bind=engine
    )


if __name__ == "__main__":

    create_tables()

    print(
        "Database tables created."
    )