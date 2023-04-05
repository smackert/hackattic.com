import requests
import json
import os
import math
from dotenv import load_dotenv
import hashlib
from json_challenge import Challenge, Block

load_dotenv()
base_url = os.getenv("CHALLENGES_BASE_URL")
problem_endpoint = os.getenv("PROBLEM_ENDPOINT")
solution_endpoint = os.getenv("SOLUTION_ENDPOINT")
access_token = os.getenv("HACKATTIC_ACCESS_TOKEN")

challenge_name = "mini_miner"
api_challenge_endpoint = base_url + challenge_name + problem_endpoint + access_token
apit_solution_endpoint = base_url + challenge_name + solution_endpoint + access_token

def get_challenge_data():
    r = requests.get(api_challenge_endpoint)
    try:
        json_data = r.json()
        return json_data
    except Exception as e:
        print(f"[!!!] Error: {e}")
        return None


def brute_force(challenge):
    hash = ""
    nonce = 0
    zeros_needed = math.ceil(challenge.difficulty / 2)
    print(f"Searching for hash with {zeros_needed} zeros")
    while hash[:zeros_needed] != (zeros_needed) * "0":
        challenge.block.nonce = nonce
        sha = hashlib.sha256()
        sha.update(json.dumps(dict(challenge.block), separators=(",", ":")).encode())
        hash = sha.hexdigest()
        if hash[:zeros_needed] == (zeros_needed) * "0":
            print(f"Match found with nonce={nonce} - ", sha.hexdigest())
            return nonce
        else:
            # print(f'[---] Nonce: {nonce} == {hash}')
            nonce += 1
            continue


def submit_solution(nonce_solution):
    print('Submitting solution..')
    r = requests.post(apit_solution_endpoint, json={'nonce': nonce_solution})
    print(f'Solution submitted. Response: {r.text}')
def main():
    challenge_data = get_challenge_data()
    challenge = Challenge.parse_obj(challenge_data)
    nonce_solution = brute_force(challenge)
    submit_solution(nonce_solution)

main()