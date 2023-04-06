from typing import List, Tuple, Optional
from pydantic import BaseModel


class Block(BaseModel):
    nonce: Optional[int]
    data: List[Tuple[str, int]]


class Challenge(BaseModel):
    difficulty: int
    block: Block
