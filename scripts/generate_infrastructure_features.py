import pandas as pd


GRID_SIZE = 0.005


def get_grid(
    latitude,
    longitude
):
    return (
        int(longitude // GRID_SIZE),
        int(latitude // GRID_SIZE)
    )


def main():

    regions = pd.read_csv(
        "data/processed/regions.csv"
    )

    amenities = pd.read_csv(
        "data/raw/chennai_amenities.csv"
    )

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

        grid = get_grid(
            row["latitude"],
            row["longitude"]
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
            "No amenities mapped"
        )

        return

    features = (
        mapped
        .pivot_table(
            index="region_id",
            columns="amenity",
            aggfunc="size",
            fill_value=0
        )
        .reset_index()
    )

    expected = [
        "police",
        "hospital",
        "school",
        "fire_station"
    ]

    for col in expected:

        if col not in features.columns:

            features[col] = 0

    features.rename(
        columns={
            "police":
                "police_count",

            "hospital":
                "hospital_count",

            "school":
                "school_count",

            "fire_station":
                "fire_station_count"
        },
        inplace=True
    )

    features[
        "amenity_count"
    ] = (
        features[
            [
                "police_count",
                "hospital_count",
                "school_count",
                "fire_station_count"
            ]
        ]
        .sum(axis=1)
    )

    features[
        "amenity_density"
    ] = (
        features[
            "amenity_count"
        ]
    )

    result = (
        regions[
            ["region_id"]
        ]
        .merge(
            features,
            on="region_id",
            how="left"
        )
        .fillna(0)
    )

    result.to_csv(
        "data/processed/infrastructure_features.csv",
        index=False
    )

    print()

    print(
        result[
            [
                "police_count",
                "hospital_count",
                "school_count",
                "fire_station_count"
            ]
        ]
        .sum()
    )

    print()

    print(
        f"Infrastructure features: {len(result)}"
    )


if __name__ == "__main__":
    main()