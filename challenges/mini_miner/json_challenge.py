from typing import List, Tuple
from dataclasses import dataclass


@dataclass
class Block:
    nonce: int
    data: List[Tuple[str, int]]

    def __post_init__(self):
        self.data = sorted(self.data, key=lambda x: x[0])


@dataclass
class Challenge:
    difficulty: int
    block: Block

    @classmethod
    def from_json(cls, json_data: dict):
        block_dict = json_data["block"]
        block_data = [(d[0], d[1]) for d in block_dict["data"]]
        block = Block(nonce=block_dict["nonce"], data=block_data)

        return cls(difficulty=json_data["difficulty"], block=block)
