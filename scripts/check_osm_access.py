import urllib.request


URLS = [
    "https://www.openstreetmap.org",
    "https://download.geofabrik.de",
]


for url in URLS:

    try:

        response = urllib.request.urlopen(
            url,
            timeout=10
        )

        print(
            f"SUCCESS: {url}"
        )

        print(
            response.status
        )

    except Exception as e:

        print(
            f"FAILED: {url}"
        )

        print(e)