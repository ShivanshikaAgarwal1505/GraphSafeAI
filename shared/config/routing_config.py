#
# Risk Fusion
#

CURRENT_RISK_WEIGHT = 0.70

PREDICTED_RISK_WEIGHT = 0.30

MAX_SAFETY_SCORE = 1.0


#
# Routing Modes
#

ROUTING_MODES = {

    "safest": {
        "risk_weight": 0.90,
        "distance_weight": 0.10
    },

    "balanced": {
        "risk_weight": 0.70,
        "distance_weight": 0.30
    },

    "fastest": {
        "risk_weight": 0.40,
        "distance_weight": 0.60
    }
}

NAVIGATION_PROFILES = {

    "walking_safe": {
        "max_detour_ratio": 1.15
    },

    "walking_balanced": {
        "max_detour_ratio": 1.05
    },

    "walking_fastest": {
        "max_detour_ratio": 1.00
    },

    "driving_safe": {
        "max_detour_ratio": 1.40
    },

    "driving_balanced": {
        "max_detour_ratio": 1.20
    },

    "driving_fastest": {
        "max_detour_ratio": 1.00
    }
}