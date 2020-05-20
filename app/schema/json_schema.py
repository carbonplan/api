import requests

metric = {
    "title": "CarbonPlan Metric",
    "type": "object",
    "required": ["type", "name", "value", "units"],
    "properties": {
        "type": {"type": "string", "enum": ["Metric"]},
        "name": {"type": "string"},
        "value": {"type": "number"},
        "units": {"type": "string"},
        "rating": {"type": "string"},
        "comment": {"type": "string"},
    },
}

revision = {
    "title": "Revision",
    "type": "object",
    "required": ["date", "note"],
    "properties": {
        "date": {"type": "string"},
        "note": {"type": "string"}
    }
}


def geojson(name):
    return requests.get(f"https://geojson.org/schema/{name}.json").json()


geometry = geojson("Feature")["properties"]["geometry"]

project = {
    "title": "CarbonPlan Project",
    "type": "object",
    "required": ["type", "name", "metrics", "geometry", "tags", "id", "description", "revisions"],
    "properties": {
        "type": {"type": "string", "enum": ["Project"]},
        "name": {"type": "string"},
        "metrics": {"type": "array", "items": metric},
        "tags": {"type": "array", "items": {"type": "string"}},
        "id": {"type": "string"},
        "description": {"type": "string"},
        "revisions": {"type": "array", "items": revision},
        "geometry": {"type": geometry},
    },
}

project_collection = {
    "title": "CarbonPlan ProjectCollection",
    "type": "object",
    "required": ["type", "projects"],
    "properties": {"type": {"type": "string", "enum": ["ProjectCollection"]}},
    "projects": {"type": "array", "items": project},
}

objects = {"ProjectCollection": project_collection, "Project": project, "Metric": metric}


def get(name):

    out = {
        "$schema": "http://json-schema.org/draft-07/schema#",
        "$id": f"https://api.carbonplan.org/schema/{name}.json",
    }

    out.update(objects[name])

    return out
