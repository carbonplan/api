import requests

metric = {
    'title': 'CarbonPlan Metric',
    'type': 'object',
    'required': ['type', 'name', 'value'],
    'properties': {
        'type': {'type': 'string', 'enum': ['Metric']},
        'name': {'type': 'string'},
        'value': {'type': 'number'},
        'rating': {'type': 'string'},
        'comment': {'type': 'string'},
    },
}


def geojson(name):
    return requests.get(f'https://geojson.org/schema/{name}.json').json()


geometry = geojson('Feature')['properties']['geometry']

project = {
    'title': "CarbonPlan Project",
    'type': "object",
    'required': ["type", "name", "metrics", "geometry", "tags", "projectId", "description",],
    'properties': {
        'type': {'type': "string", 'enum': ["Project"]},
        'name': {'type': "string"},
        'metrics': {'type': "array", 'items': metric},
        'tags': {'type': "array", 'items': {'type': "string"}},
        'projectId': {'type': "string"},
        'description': {'type': "string"},
        'geometry': {'type': geometry,},
    },
}

objects = {'Project': project, 'Metric': metric}


def get(name):

    out = {
        '$schema': 'http://json-schema.org/draft-07/schema#',
        '$id': f'https://api.carbonplan.org/schema/{name}.json',
    }

    out.update(objects[name])

    return out
