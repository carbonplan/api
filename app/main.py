from fastapi import FastAPI, Request


app = FastAPI()

# Return a Cache-Control header for all requests.
# The no-cache directive disables caching on the zeit CDN.
# Including this better demonstrates using FastAPI as a
# serverless function.
@app.middleware("http")
async def add_no_cache_header(request: Request, call_next):
    response = await call_next(request)
    response.headers["Cache-Control"] = "no-cache"
    return response


@app.get('/')
@app.get('/hello')
def hello():
    return {'hello': 'world!!'}
