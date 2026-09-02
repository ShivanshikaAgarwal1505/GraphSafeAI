from math import sqrt


def euclidean_distance(
    lat1,
    lon1,
    lat2,
    lon2
):
    return sqrt(
        (lat1 - lat2) ** 2 +
        (lon1 - lon2) ** 2
    )