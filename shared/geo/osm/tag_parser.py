import re


def extract_tag(
    tag_string,
    key
):
    if not isinstance(
        tag_string,
        str
    ):
        return None

    pattern = (
        rf'"{key}"=>"(.*?)"'
    )

    match = re.search(
        pattern,
        tag_string
    )

    if match:
        return match.group(1)

    return None