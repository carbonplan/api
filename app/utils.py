import pathlib

import pandas as pd

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


def projects_to_csv(projects, id=None):
    print("projects", projects)
    df = pd.DataFrame.from_dict(projects).set_index("id").drop(columns=["type", "geometry"])

    metrics = {}
    sources = {}
    tags = {}
    for i, row in df.iterrows():

        # metrics
        metrics[i] = pd.DataFrame(row.metrics).set_index("name").drop(columns="type").stack()

        # source
        sources[i] = pd.Series(row.source)
        sources[i].index = [("source", name) for name in sources[i].index]

        # tags
        tags[i] = pd.Series(row.tags)
        tags[i].index = [("tag", name) for name in tags[i].index]

    metrics = pd.DataFrame.from_dict(metrics, orient="index")
    sources = pd.DataFrame.from_dict(sources, orient="index")
    tags = pd.DataFrame.from_dict(tags, orient="index")

    drop = ["metrics", "location", "source", "tags"]

    out = pd.concat([df.drop(columns=drop), metrics, sources, tags], axis=1)

    if id:
        out = out.loc[[id]]

    return out.to_csv()
