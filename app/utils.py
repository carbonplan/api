import pathlib

# custom openapi schema info
INFO = {
    "termsOfService": "https://carbonplan.org/terms",
    "contact": {"email": "hello@carbonplan.org"},
    "license": {
        "name": "MIT",
        "url": "https://raw.githubusercontent.com/carbonplan/api/master/LICENSE",
    },
    "x-logo": {"url": "https://carbonplan-assets.s3.amazonaws.com/images/social.png"},
}


def get_title_and_description():
    """helper function to read and parse README.md"""
    readme = pathlib.Path(__file__).parents[0] / "README.md"
    with open(readme, "r") as f:
        lines = f.readlines()
        header = lines[0].strip().replace("#", "")
    return header, "\n".join(lines[1:])
