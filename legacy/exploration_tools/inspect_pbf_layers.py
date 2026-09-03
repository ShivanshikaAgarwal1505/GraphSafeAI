import pyogrio

PBF_PATH = (
    r"C:\Users\T9978\Projects\ProjectCodes"
    r"\Railway-AI-Traffic-Optimization"
    r"\data\raw\india-latest.osm.pbf"
)


def main():

    layers = pyogrio.list_layers(
        PBF_PATH
    )

    print(layers)


if __name__ == "__main__":
    main()