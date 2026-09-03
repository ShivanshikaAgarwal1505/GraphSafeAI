from GraphSafeAIv2.shared.geo.region_mapper import (
    RegionMapper
)


def main():

    mapper = RegionMapper()

    region_id = mapper.find_region(
        latitude=13.0827,
        longitude=80.2707
    )

    print()
    print("Region:", region_id)


if __name__ == "__main__":
    main()