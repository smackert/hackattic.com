import os
import json
import struct
import base64
import dotenv
import requests


# https://hackattic.com/challenges/help_me_unpack
# 4 byte ints - everything is 32-bit platform
# pack = int, uint, short, float, double, big_endian_double
# bytes = 4 , 4, 2, 4, 8, 8 =

dotenv.load_dotenv()
acces_token = os.getenv("HACKATTIC_ACCESS_TOKEN")
base_url = os.getenv("CHALLENGES_BASE_URL")
problem_endpoint = os.getenv("PROBLEM_ENDPOINT")
solution_endpoint = os.getenv("SOLUTION_ENDPOINT")
challenge_name = "help_me_unpack"

api_challenge_endpoint = base_url + challenge_name + problem_endpoint + acces_token
api_solution_endpoint = base_url + challenge_name + solution_endpoint + acces_token

try:
    r = requests.get(api_challenge_endpoint)
    r_bytes = r.json()["bytes"]
except Exception as e:
    print(f"Error: {e}")

print(f"Got bytes: {r_bytes}")

decoded_bytes = base64.b64decode(r_bytes)
print(decoded_bytes)

s_int = struct.unpack("i", decoded_bytes[:4])[0]
u_int = struct.unpack("I", decoded_bytes[4:8])[0]
short = struct.unpack("h", decoded_bytes[8:10])[0]
float_v = struct.unpack("f", decoded_bytes[12:16])[0]
double = struct.unpack("d", decoded_bytes[16:24])[0]
be_double = struct.unpack("!d", decoded_bytes[24:32])[0]

solution = {
    "int": s_int,
    "uint": u_int,
    "short": short,
    "float": float_v,
    "double": double,
    "big_endian_double": be_double,
}

try:
    r = requests.post(api_solution_endpoint, json=solution)
    print(r.text)
except Exception as e:
    print(f"Error: {e}")
