# CarbonPlan Projects API

![CI](https://github.com/carbonplan/api/workflows/CI/badge.svg)

This repository includes CarbonPlan's Projects API.

## Usage Documentation

For usage documentation of the API, see https://api.carbonplan.org/docs.

-----

## Developer Documentation

This API is a [FastAPI application](https://fastapi.tiangolo.com/). To run the API locally use:

```shell
$ uvicorn app.main:app --reload
```

Currently we are storing all metrics within a JSON file in this repository (see `./app/data/projects.json`), derived from a Google Sheet.

To generate a fresh copy of the metrics based on the latest Google Sheet, make sure you have Google credentials stored in a file local to this repository called `key.json` and then run:

```shell
$ python scripts/build_projects.py
```

To run the unit and integration tests for this API, run:

```shell
$ py.test -v
```
