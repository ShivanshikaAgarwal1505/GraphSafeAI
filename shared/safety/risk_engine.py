import math


def normalize(
    value,
    min_value,
    max_value
):

    if max_value == min_value:
        return 0

    return (
        value - min_value
    ) / (
        max_value - min_value
    )


def calculate_incident_confidence(
    report_count
):

    return (
        1 -
        math.exp(
            -report_count / 10
        )
    )


def calculate_weights(
    report_count
):

    incident_confidence = (
        calculate_incident_confidence(
            report_count
        )
    )

    structural_confidence = 1.0

    total = (
        structural_confidence
        +
        incident_confidence
    )

    return {

        "incident_confidence":
            incident_confidence,

        "structural_weight":
            structural_confidence
            / total,

        "incident_weight":
            incident_confidence
            / total,
    }