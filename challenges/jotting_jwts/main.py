from fastapi import FastAPI, Request, Body
import utils
from starlette.requests import Request
from starlette.responses import Response
import json
import asyncio

app = FastAPI()


@app.on_event("startup")
async def startup_event():
    global secret_string, jwt_secret
    secret_string = ''
    jwt_secret = utils.get_jwt_secret()
    asyncio.create_task(utils.submit_app())

@app.post("/", response_class=Response)
async def root(request: Request):
    global secret_string, jwt_secret
    request_data = await request.body()
    print(f"[+++] New post request: {request_data} with {type(request_data)}")
    try:
        append_string = utils.decode_jwt(request_data, jwt_secret)
        print(f"[+++] New append string: {append_string}")
        secret_string = secret_string + append_string
    except:
        print(f"[+++] Request ignored")
    return  request_data


