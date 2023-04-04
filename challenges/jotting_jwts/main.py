from fastapi import FastAPI, Request, Body
import utils
from starlette.requests import Request
from starlette.responses import Response
import asyncio
import time

app = FastAPI()

@app.on_event("startup")
async def startup_event():
    global solution, jwt_secret
    global time_start
    solution = ''
    jwt_secret = await utils.get_jwt_secret()
    time_start = time.time()
    asyncio.create_task(utils.submit_app())

@app.post("/", response_class=Response)
async def root(request: Request):
    global solution, jwt_secret
    request_data = await request.body()
    # print(f"[+++] New post request: {request_data} with {type(request_data)}")
    append_string, is_finalToken = await utils.decode_jwt(request_data, jwt_secret)
    if append_string:
        print(f"[+++] New append string: {append_string}")
        solution = solution + append_string
    elif is_finalToken:
        asyncio.create_task(utils.submit_solution(solution))
        tot_time = time.time() - time_start
        print(f'Total time: {tot_time}')
        return None
    else:
        print(f"[+++] String could not be read. Ignoring")


