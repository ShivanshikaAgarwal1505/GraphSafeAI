import pandas as pd


class RegionMapper:

    GRID_SIZE = 0.005

    def __init__(self):

        self.regions = pd.read_csv(
            "data/processed/regions.csv"
        )

    def find_region(
        self,
        latitude: float,
        longitude: float
    ):

        grid_x = int(
            longitude //
            self.GRID_SIZE
        )

        grid_y = int(
            latitude //
            self.GRID_SIZE
        )

        match = self.regions[
            (self.regions["grid_x"] == grid_x)
            &
            (self.regions["grid_y"] == grid_y)
        ]

        if len(match) == 0:
            return None

        return int(
            match.iloc[0]["region_id"]
        )