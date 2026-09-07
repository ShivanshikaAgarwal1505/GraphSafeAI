from enum import Enum


class ReportSource(
    str,
    Enum
):
    CITIZEN = "CITIZEN"

    AUTHORITY = "AUTHORITY"

    PARTNER = "PARTNER"

    SYSTEM = "SYSTEM"