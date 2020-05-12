import json
import pathlib
from functools import lru_cache

from fastapi import FastAPI, Request
from fastapi.responses import PlainTextResponse
from starlette.exceptions import HTTPException as StarletteHTTPException

from .schema import json_schema

app = FastAPI()

app_dir = pathlib.Path(__file__).parent


def IndentedResponse(obj, **kwargs):
    return PlainTextResponse(json.dumps(obj, indent=2), **kwargs)


def AppException(status_code=404):
    data = {"message": "Not Found", "documentation_url": "https://api.carbonplan.org/docs"}
    return IndentedResponse(data, status_code=status_code)


@app.exception_handler(StarletteHTTPException)
async def http_exception_handler(request, exc):
    return AppException(status_code=exc.status_code)


@lru_cache(maxsize=32, typed=False)
def get_data(kind):
    if kind == "projects":
        with open(app_dir / "data" / "projects.json", "r") as f:
            return json.load(f)
    else:
        raise NotImplementedError(kind)


# Return a Cache-Control header for all requests.
# The no-cache directive disables caching on the zeit CDN.
# Including this better demonstrates using FastAPI as a
# serverless function.
@app.middleware("http")
async def add_no_cache_header(request: Request, call_next):
    response = await call_next(request)
    response.headers["Cache-Control"] = "no-cache"
    return response


@app.get("/")
def root():
    return IndentedResponse(
        {
            "projects_url": "https://api.carbonplan.org/projects",
            "schema_url": "https://api.carbonplan.org/schema",
        }
    )


@app.get("/projects")
def projects(id: str = None):
    data = get_data("projects")

    out = {}
    if id is None:
        out = data

    for p in data["projects"]:
        if p["id"] == id:
            out = p
            break

    return IndentedResponse(out)


@app.get("/schema")
def schema(obj: str = None):
    summary = {"objects": list(json_schema.objects.keys())}
    return IndentedResponse(summary)


@app.get("/schema/{obj}.json")
def schema_obj(obj: str):
    try:
        return IndentedResponse(json_schema.get(obj))
    except KeyError:
        return AppException()
