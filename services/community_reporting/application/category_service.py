from sqlalchemy import func

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

    def get_category_stats(
        self,
        db
    ):

        rows = (
            db.query(
                CommunityReport.category,
                func.count(
                    CommunityReport.id
                )
            )
            .group_by(
                CommunityReport.category
            )
            .all()
        )

        return {
            category: count
            for category, count in rows
        }