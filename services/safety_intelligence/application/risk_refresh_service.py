from sqlalchemy import or_

from shared.database.models.region_edge import (
    RegionEdge
)

from services.safety_intelligence.application.safety_feature_service import (
    SafetyFeatureService
)

from services.safety_intelligence.application.risk_score_service import (
    RiskScoreService
)

import logging
import time

logger = logging.getLogger(__name__)

class RiskRefreshService:

    def __init__(self):

        self.feature_service = (
            SafetyFeatureService()
        )

        self.risk_service = (
            RiskScoreService()
        )

    def refresh_all(
        self,
        db
    ):

        self.feature_service.generate_all(
            db
        )

        self.risk_service.calculate_all(
            db
        )

    def refresh_region_and_neighbors(
        self,
        db,
        region_id: int
    ):
        start_time = time.perf_counter()
        region_ids = {
            region_id
        }

        edges = (
            db.query(
                RegionEdge
            )
            .filter(
                or_(
                    RegionEdge.source_region_id
                    == region_id,

                    RegionEdge.target_region_id
                    == region_id
                )
            )
            .all()
        )

        for edge in edges:

            region_ids.add(
                edge.source_region_id
            )

            region_ids.add(
                edge.target_region_id
            )
        

        for current_region_id in region_ids:

            self.feature_service.generate_region(
                db,
                current_region_id
            )

        for current_region_id in region_ids:

            self.risk_service.calculate_region(
                db,
                current_region_id
            )
            
        
        logger.info(
            "[RISK_REFRESH] region=%s",
            region_id
        )

        logger.info(
            "[RISK_REFRESH] affected_regions=%s",
            sorted(region_ids)
        )
        db.commit()

        elapsed = (
        time.perf_counter()
        - start_time
        )

        logger.info(
        "[RISK_REFRESH] completed in %.3fs",
        elapsed
        )
        
        