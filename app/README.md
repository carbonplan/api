# (carbon)plan / API

## overview

This API provides access to our data on carbon removal projects. If you have any problems or questions, please [send us an email](mailto:hello@carbonplan.org) or open a [GitHub Issue](https://github.com/carbonplan/api).

## current version

This is `v0` of the Projects REST API. You can explicitly request this version of the API by specifying the version as a prefix in API urls. For example,

```
https://api.carbonplan.org/{version}/{endpoint}
# or
https://api.carbonplan.org/v0/projects.json
```

When the version prefix is not provided, the API will route requests to the current stable version of the API.

```shell
$ curl -i https://api.carbonplan.org/v0/projects.json?id=STRP02
HTTP/1.1 200 OK
Date: Tue, 12 May 2020 19:25:41 GMT
Content-Type: application/json; charset=utf-8
Connection: keep-alive
X-Robots-Tag: noindex
cache-control: no-cache
content-length: 161
age: 0
strict-transport-security: max-age=63072000; includeSubDomains; preload
{
  "type": "ProjectCollection",
  "projects": [
    {
      "type": "Project",
      "name": "Climeworks",
      "metrics": [
        {
          "type": "Metric",
          "name": "mechanism",
...
```

## schema

The API is accessed over HTTPS at `https://api.carbonplan.org`. All data is sent and recieved as JSON. The full JSON schema is available at `https://api.carbonplan.org/{version}/schema/{object}.json` where `{object}` one of the following:

- `Project`: A JSON object defining a single carbon removal project. Click [here](../schema/Project.json) to see the full schema.
- `ProjectCollection`: A JSON object defining a group of `Project`s. Click [here](../schema/ProjectCollection.json) to see the full schema.
- `Metric`: A JSON object defining a single metric about a specific `Project`. Click [here](../schema/Metric.json) to see the full schema.
