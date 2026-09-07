import pandas as pd
import numpy as np

from shared.geo.osm.amenity_config import (
    AMENITY_TYPES
)


def haversine(
    lat1,
    lon1,
    lat2,
    lon2
):
    """
    Distance in kilometers.
    """

    r = 6371.0

    lat1 = np.radians(lat1)
    lon1 = np.radians(lon1)

    lat2 = np.radians(lat2)
    lon2 = np.radians(lon2)

    dlat = lat2 - lat1
    dlon = lon2 - lon1

    a = (
        np.sin(dlat / 2) ** 2
        +
        np.cos(lat1)
        *
        np.cos(lat2)
        *
        np.sin(dlon / 2) ** 2
    )

    c = (
        2
        *
        np.arcsin(
            np.sqrt(a)
        )
    )

    return r * c


def nearest_distance(
    region_lat,
    region_lon,
    amenity_df
):
    if amenity_df.empty:
        return -1.0

    distances = haversine(
        region_lat,
        region_lon,
        amenity_df["latitude"].values,
        amenity_df["longitude"].values,
    )

    return float(
        distances.min()
    )


def main():

    regions = pd.read_csv(
        "data/processed/regions.csv"
    )

    node_counts = (
        regions[
            ["region_id", "node_count"]
        ]
        .copy()
    )

    amenities = pd.read_csv(
        "data/raw/chennai_amenities.csv"
    )

    grid_size = 0.005

    lookup = {}

    for _, row in regions.iterrows():

        lookup[
            (
                int(row["grid_x"]),
                int(row["grid_y"])
            )
        ] = row["region_id"]

    records = []

    for _, row in amenities.iterrows():

        grid = (
            int(
                row["longitude"]
                // grid_size
            ),
            int(
                row["latitude"]
                // grid_size
            )
        )

        region_id = lookup.get(
            grid
        )

        if region_id is None:
            continue

        records.append(
            {
                "region_id":
                    region_id,

                "amenity":
                    row["amenity"]
            }
        )

    mapped = pd.DataFrame(
        records
    )

    if mapped.empty:

        print(
            "No amenities mapped."
        )

        return

    counts = (
        mapped
        .pivot_table(
            index="region_id",
            columns="amenity",
            aggfunc="size",
            fill_value=0
        )
        .reset_index()
    )

    #
    # Ensure all amenity columns exist
    #

    for amenity in AMENITY_TYPES:

        if amenity not in counts.columns:

            counts[
                amenity
            ] = 0

    #
    # Rename dynamically
    #

    counts.rename(
        columns={
            amenity:
                f"{amenity}_count"
            for amenity in AMENITY_TYPES
        },
        inplace=True
    )

    count_columns = [
        f"{amenity}_count"
        for amenity in AMENITY_TYPES
    ]

    #
    # Total amenity statistics
    #

    counts["amenity_count"] = (
        counts[count_columns]
        .sum(axis=1)
    )

    counts["amenity_density"] = (
        counts["amenity_count"]
    )

    #
    # Dynamic density features
    #

    for amenity in AMENITY_TYPES:

        count_col = (
            f"{amenity}_count"
        )

        density_col = (
            f"{amenity}_density"
        )

        counts[density_col] = (
            counts[count_col]
        )

    #
    # Amenity datasets for distance calculations
    #

    amenity_frames = {}

    for amenity in AMENITY_TYPES:

        amenity_frames[
            amenity
        ] = amenities[
            amenities["amenity"]
            == amenity
        ]

    #
    # Distance features
    #

    print(
        "Calculating nearest distances..."
    )

    distance_rows = []

    for _, region in regions.iterrows():

        lat = region[
            "center_lat"
        ]

        lon = region[
            "center_lon"
        ]

        row_data = {
            "region_id":
                region["region_id"]
        }

        for amenity in AMENITY_TYPES:

            row_data[
                f"nearest_{amenity}_distance"
            ] = nearest_distance(
                lat,
                lon,
                amenity_frames[
                    amenity
                ]
            )

        distance_rows.append(
            row_data
        )

    distance_df = pd.DataFrame(
        distance_rows
    )

    #
    # Merge everything
    #

    result = (
        node_counts
        .merge(
            counts,
            on="region_id",
            how="left"
        )
        .merge(
            distance_df,
            on="region_id",
            how="left"
        )
        .fillna(0)
    )
    #
    # Per-node density features
    #

    safe_nodes = (
        result["node_count"]
        .replace(0, 1)
    )

    for amenity in AMENITY_TYPES:

        count_col = (
            f"{amenity}_count"
        )

        per_node_col = (
            f"{amenity}_per_node"
        )

        if count_col in result.columns:

            result[per_node_col] = (
                result[count_col]
                /
                safe_nodes
            )

    result.to_csv(
        "data/processed/infrastructure_features.csv",
        index=False
    )

    print()

    print(
        f"Infrastructure features: {len(result)}"
    )

    print()

    print(
        "Amenities configured:"
    )

    print(
        AMENITY_TYPES
    )

    print()

    print(
        result.head()
    )


if __name__ == "__main__":
    main()