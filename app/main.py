
from fastapi import FastAPI


app = FastAPI()


@app.get('/')
@app.get('/hello')
def hello():
    return {'hello': 'world!!'}
