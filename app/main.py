import json
import pathlib
import typing
from functools import lru_cache

from fastapi import FastAPI, Request
from fastapi.openapi.utils import get_openapi
from starlette.exceptions import HTTPException as StarletteHTTPException
from starlette.responses import PlainTextResponse, Response

from . import __version__ as VERSION
from .schema import json_schema
from .utils import INFO, get_title_and_description, projects_to_csv

CHARSET = "utf-8"

app_dir = pathlib.Path(__file__).parent


class PrettyJSONResponse(Response):
    """ A pretty JSON response class """

    media_type = f"application/json; charset={CHARSET}"

    def render(self, content: typing.Any) -> bytes:
        return json.dumps(content, indent=2).encode(CHARSET)


def AppException(status_code=404):
    """ A custom exception to point users to documentation url """
    data = {"message": "Not Found", "documentation_url": "https://api.carbonplan.org/docs"}
    return PrettyJSONResponse(data, status_code=status_code)


@lru_cache(maxsize=32, typed=False)
def get_data(kind):
    """ load the projects dataset """
    if kind == "projects":
        with open(app_dir / "data" / "projects.json", "r") as f:
            return json.load(f)
    else:
        raise NotImplementedError(kind)


# create FAST APP App
app = FastAPI(default_response_class=PrettyJSONResponse)


@app.exception_handler(StarletteHTTPException)
async def http_exception_handler(request, exc):
    """ Custom exception handler """
    return AppException(status_code=exc.status_code)


@app.middleware("http")
async def add_custom_header(request: Request, call_next):
    """ inject a few custom headers into app """
    response = await call_next(request)
    response.headers["Cache-Control"] = "no-cache"
    response.headers["x-carbonplan-media-type"] = f"carbonplan.{VERSION}; format=json"
    return response


@app.get("/")
@app.get(f"/{VERSION}/", include_in_schema=False)
def root():
    """ base endpoint for API """
    return {
        "docs_url": "https://api.carbonplan.org/docs",
        "schema_url": "https://api.carbonplan.org/schema.json",
        "projects_url": "https://api.carbonplan.org/projects.json",
    }


@app.get("/projects.json")
@app.get(f"/{VERSION}/projects.json", include_in_schema=False)
def projects(id: str = None):
    """ return a `ProjectCollection` if `id` is None, otherwise return a `Project`"""
    data = get_data("projects")

    out = {}
    if id is None:
        out = data

    for p in data["projects"]:
        if p["id"] == id:
            out = p
            break

    return out


@app.get("/projects.csv")
@app.get(f"/{VERSION}/projects.csv", include_in_schema=False)
def projects_csv(id: str = None):
    """ return a `ProjectCollection` if `id` is None, otherwise return a `Project`"""
    data = get_data("projects")

    csv = projects_to_csv(data["projects"], id)

    return PlainTextResponse(csv, media_type="text/csv")


@app.get("/schema.json")
@app.get(f"/{VERSION}/schema.json", include_in_schema=False)
def schema(obj: str = None):
    """ return a the list of objects defined in the schema """
    return {"objects": list(json_schema.objects.keys())}


@app.get("/schema/{obj}.json")
@app.get(f"/{VERSION}/schema/{{obj}}.json", include_in_schema=False)
def schema_object(obj: str):
    """Return the schema for `obj`"""
    try:
        return json_schema.get(obj)
    except KeyError:
        return AppException()


def custom_openapi():
    """function to set custom OpenAPI schema"""
    if app.openapi_schema:
        return app.openapi_schema

    title, description = get_title_and_description()

    openapi_schema = get_openapi(
        title=title, version=VERSION, description=description, routes=app.routes,
    )

    openapi_schema["info"].update(INFO)

    app.openapi_schema = openapi_schema

    return app.openapi_schema


# set custom openapi schema
app.openapi = custom_openapi
