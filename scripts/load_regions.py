from shared.database.session import SessionLocal

from shared.database.models.region import Region

from shared.geo.grid_generator import (
    ChennaiGridGenerator
)


def load_regions():

    db = SessionLocal()

    existing_count = db.query(Region).count()

    if existing_count > 0:
        print(
            f"Regions already exist ({existing_count})."
        )
        db.close()
        return

    generator = ChennaiGridGenerator()

    regions = generator.generate()

    for region in regions:

        db.add(
            Region(
                region_name=region.region_name,
                centroid_lat=region.centroid_lat,
                centroid_lon=region.centroid_lon
            )
        )

    db.commit()

    print(
        f"{len(regions)} regions inserted."
    )

    db.close()


if __name__ == "__main__":
    load_regions()