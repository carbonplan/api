from functools import lru_cache

import json

from fastapi import FastAPI, Request


app = FastAPI()


@lru_cache
def get_data(kind):
    if kind == 'projects':
        with open('projects.json', 'r') as f:
            return json.load(f)
    else:
        raise NotImplementedError(kind)


# Return a Cache-Control header for all requests.
# The no-cache directive disables caching on the zeit CDN.
# Including this better demonstrates using FastAPI as a
# serverless function.
@app.middleware('http')
async def add_no_cache_header(request: Request, call_next):
    response = await call_next(request)
    response.headers['Cache-Control'] = 'no-cache'
    return response


@app.get('/projects')
def projects(id: str = None):
    data = get_data('projects')

    if id is None:
        return data

    for p in data['features']:
        if p['project_id'] == id:
            return p

    return {}
