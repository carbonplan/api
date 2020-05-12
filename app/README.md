# CarbonPlan Projects API

## Overview

The CarbonPlan Projects API provides access to our collection of carbon removal projects. If you have any problems or questions, please [send us an email](mailto:hello@carbonplan.org) or open a [GitHub Issue](https://github.com/carbonplan/api).

## Current version

This is `v0` of the Projects REST API. You can explicitly request this version of the API via the `Accept` header.

```shell
$ curl -i https://api.carbonplan.org
HTTP/1.1 200 OK
Date: Tue, 12 May 2020 19:25:41 GMT
Content-Type: application/json; charset=utf-8
Connection: keep-alive
X-Robots-Tag: noindex
cache-control: no-cache
x-carbonplan-media-type: carbonplan.v0; format=json
content-length: 161
x-vercel-cache: MISS
x-now-cache: MISS
age: 0
x-now-trace: pdx1
server: now
x-vercel-id: pdx1::sfo1::9cvcd-1589311541284-3d0f4584205c
x-now-id: pdx1::sfo1::9cvcd-1589311541284-3d0f4584205c
strict-transport-security: max-age=63072000; includeSubDomains; preload
```

## Schema

The API is accessed over HTTPS at `https://api.carbonplan.org`. All data is sent and recieved as JSON. The full JSON schema is available at `https://api.carbonplan.org/schema/{object}.json` where `{object}` one of the following:

- `Project`: A JSON object defining a single carbon removal project. Click [here](../schema/Project.json) to see the full schema.
- `ProjectCollection`: A JSON object defining a group of `Project`s. Click [here](../schema/ProjectCollection.json) to see the full schema.
- `Metric`: A JSON object defining a single metric about a specific `Project`. Click [here](../schema/Metric.json) to see the full schema.
