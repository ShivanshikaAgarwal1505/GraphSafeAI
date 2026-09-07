from enum import Enum


class ReportStatus(
    str,
    Enum
):
    OPEN = "OPEN"

    RESOLVED = "RESOLVED"

    REJECTED = "REJECTED"