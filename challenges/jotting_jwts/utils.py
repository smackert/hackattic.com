import httpx
import requests
import os
from dotenv import load_dotenv
import json
import jwt

load_dotenv()
access_token = os.getenv('HACKATTIC_ACCESS_TOKEN')
app_url = os.getenv('MY_APP_URL')

base_url = 'https://hackattic.com/challenges/jotting_jwts'
api_problem_endpoint = base_url + '/problem?access_token=' + access_token
api_submission_endpoint = base_url + '/solve?access_token=' + access_token

async def get_jwt_secret():
    r = requests.get(api_problem_endpoint)
    jwt_data = json.loads(r.text)
    print(f'[+++] Got jwt secret: {jwt_data["jwt_secret"]}')
    return jwt_data['jwt_secret']

async def submit_app():
    print(f'[+++] Submitting app url...')
    app_url_data = {'app_url': app_url}
    try:
        async with httpx.AsyncClient(timeout=1) as client:
            r = await client.post(api_submission_endpoint, json=app_url_data)
    except httpx.TimeoutException:
        print("Timedout")

async def decode_jwt(encoded_token, jwt_secret):
    try:
        decoded_token= jwt.decode(encoded_token, jwt_secret, algorithms=['HS256'])
        append_string = decoded_token.get('append')
        if append_string:
            return (append_string, True)
        else:
            print(f'[+++] Final token recieved.')
            return (None, True) 
    except Exception as e:
        print(f"[!!!] Could not decode token. Error: {e}")
        return (None, False)
