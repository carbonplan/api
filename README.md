# (carbon)plan / API

![CI](https://github.com/carbonplan/api/workflows/CI/badge.svg)
![status](https://badgen.net/uptime-robot/status/m784948136-95d37dbf3887fb1e45468070)
![uptime](https://badgen.net/uptime-robot/month/m784948136-95d37dbf3887fb1e45468070)

This repository includes our API for data on carbon removal projects. To browse the data served by this API in an interactive dashboard, check out [carbonplan.org/reports](https://carbonplan.org/reports).

## usage documentation

For usage documentation on the API, see https://api.carbonplan.org/docs.

-----

## developer documentation

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

## license

All the code in this repository is MIT licensed. Some of the data provided by this API is sourced from content made available under a CC-BY license. We include attribution for this content, and we please request that you also maintain that attribution if using this data.

## about us

CarbonPlan is a non-profit organization that uses data and science for carbon removal. We aim to improve the transparency and scientific integrity of carbon removal and climate solutions through open data and tools. Find out more at [carbonplan.org](https://carbonplan.org/) or get in touch by [opening an issue](https://github.com/carbonplan/api/issues/new) or [sending us an email](mailto:hello@carbonplan.org).

