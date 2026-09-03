from pathlib import Path

from shared.geo.osm.amenity_extractor import (
    AmenityExtractor
)


def main():

    amenities = (
        AmenityExtractor()
        .extract()
    )

    print()

    print(
        amenities["amenity"]
        .value_counts()
    )

    output = Path(
        "data/raw/chennai_amenities.csv"
    )

    amenities.to_csv(
        output,
        index=False
    )

    print()

    print(
        f"Saved {len(amenities)} amenities"
    )

    print(
        f"File: {output}"
    )


if __name__ == "__main__":
    main()