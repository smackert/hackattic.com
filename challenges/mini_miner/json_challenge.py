from typing import List, Tuple, Optional
from pydantic import BaseModel

class Block(BaseModel):
    nonce: Optional[int]
    data: List[Tuple[str, int]]

    def __post_init__(self):
        self.data = sorted(self.data, key=lambda x: x[0])


class Challenge(BaseModel):
    difficulty: int
    block: Block
