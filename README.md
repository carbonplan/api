<img
  src='https://carbonplan-assets.s3.amazonaws.com/monogram/dark-small.png'
  height='48'
/>

# carbonplan / api

**former api for carbonplan data**

This project has been retired. See https://carbonplan.org/research/cdr-database for current data listings.

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

All the code in this repository is [MIT](https://choosealicense.com/licenses/mit/) licensed. Some of the data provided by this API is sourced from content made available under a [CC-BY-4.0](https://choosealicense.com/licenses/cc-by-4.0/) license. We include attribution for this content, and we please request that you also maintain that attribution if using this data.

## about us

CarbonPlan is a non-profit organization that uses data and science for carbon removal. We aim to improve the transparency and scientific integrity of carbon removal and climate solutions through open data and tools. Find out more at [carbonplan.org](https://carbonplan.org/) or get in touch by [opening an issue](https://github.com/carbonplan/api/issues/new) or [sending us an email](mailto:hello@carbonplan.org).
