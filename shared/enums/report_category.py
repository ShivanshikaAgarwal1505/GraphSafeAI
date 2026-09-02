from enum import Enum


class ReportCategory(str, Enum):
    POOR_LIGHTING = "poor_lighting"
    HARASSMENT = "harassment"
    SUSPICIOUS_ACTIVITY = "suspicious_activity"
    ROAD_BLOCK = "road_block"
    CROWDING = "crowding"
    UNSAFE_AREA = "unsafe_area"