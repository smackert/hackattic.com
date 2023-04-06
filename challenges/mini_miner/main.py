import requests
import json
import os
import math
from dotenv import load_dotenv
import hashlib
from json_challenge import Challenge, Block
from multiprocessing import Process, Queue

load_dotenv()
base_url = os.getenv("CHALLENGES_BASE_URL")
problem_endpoint = os.getenv("PROBLEM_ENDPOINT")
solution_endpoint = os.getenv("SOLUTION_ENDPOINT")
access_token = os.getenv("HACKATTIC_ACCESS_TOKEN")

challenge_name = "mini_miner"
api_challenge_endpoint = base_url + challenge_name + problem_endpoint + access_token
api_solution_endpoint = base_url + challenge_name + solution_endpoint + access_token


def get_challenge_data():
    r = requests.get(api_challenge_endpoint)
    try:
        json_data = r.json()
        return json_data
    except Exception as e:
        print(f"[!!!] Error: {e}")
        return None


def get_hash(challenge, start_nonce, step, zeros_needed, result_queue):
    nonce = start_nonce
    while True:
        challenge.block.nonce = nonce
        sha = hashlib.sha256()
        sha.update(
            json.dumps(dict(sorted(challenge.block)), separators=(",", ":")).encode()
        )
        hash = sha.hexdigest()
        if hash[:zeros_needed] == (zeros_needed) * "0":
            print(f"Match found with nonce={nonce} - ", sha.hexdigest())
            result_queue.put(nonce)
            return
        else:
            nonce += step


def brute_force(challenge, num_processes):
    zeros_needed = math.ceil(challenge.difficulty / 4)
    print(f"Searching for hash with {zeros_needed} zeros")
    result_queue = Queue()
    processes = []

    for i in range(num_processes):
        nonce = i
        step = num_processes
        process = Process(
            target=get_hash, args=(challenge, nonce, step, zeros_needed, result_queue)
        )
        process.start()
        processes.append(process)

    for process in processes:
        process.join()

    while not result_queue.empty():
        result = result_queue.get()
        print(f"Found match: {result}")
        return result


def submit_solution(nonce_solution):
    print("Submitting solution..")
    r = requests.post(api_solution_endpoint, json={"nonce": nonce_solution})
    print(f"Solution submitted. Response: {r.text}")


def main():
    challenge_data = get_challenge_data()
    challenge = Challenge.parse_obj(challenge_data)
    nonce_solution = brute_force(challenge, 8)
    submit_solution(nonce_solution)


if __name__ == "__main__":
    main()
