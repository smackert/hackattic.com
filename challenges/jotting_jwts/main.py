from fastapi import FastAPI, Request, Body
import utils
from starlette.requests import Request
from starlette.responses import Response
import json
import asyncio

app = FastAPI()


@app.on_event("startup")
async def startup_event():
    global solution, jwt_secret
    solution = ''
    jwt_secret = utils.get_jwt_secret()
    asyncio.create_task(utils.submit_app())

@app.post("/", response_class=Response)
async def root(request: Request):
    global solution, jwt_secret
    request_data = await request.body()
    print(f"[+++] New post request: {request_data} with {type(request_data)}")
    append_string, is_finalToken = utils.decode_jwt(request_data, jwt_secret)
    if append_string:
        print(f"[+++] New append string: {append_string}")
        solution = solution + append_string
    elif is_finalToken:
        await utils.submit_solution(solution)
    else:
        print(f"[+++] String could not be read. Ignoring")


