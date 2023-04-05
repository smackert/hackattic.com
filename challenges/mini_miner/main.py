import requests
import json
import os
from dotenv import load_dotenv
import hashlib
from json_challenge import Challenge, Block

load_dotenv()
base_url = os.getenv("CHALLENGES_BASE_URL")
problem_endpoint = os.getenv("PROBLEM_ENDPOINT")
access_token = os.getenv("HACKATTIC_ACCESS_TOKEN")

challenge_name = "mini_miner"
api_challenge_endpoint = base_url + challenge_name + problem_endpoint + access_token


def get_challenge_data():
    r = requests.get(api_challenge_endpoint)
    try:
        json_data = r.json()
        return json_data
    except Exception as e:
        print(f"[!!!] Error: {e}")
        return None


challenge_data = get_challenge_data()
challenge = Challenge.from_json(challenge_data)

# print(challenge.block)
print(json.dumps(challenge.block.data, separators=(",", ":")))