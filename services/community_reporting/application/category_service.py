from shared.database.models.community_report import (
    CommunityReport
)


class CategoryService:

    def get_categories(
        self,
        db
    ):

        rows = (
            db.query(
                CommunityReport.category
            )
            .distinct()
            .all()
        )

        return sorted(
            [
                row[0]
                for row in rows
            ]
        )