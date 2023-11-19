from pydantic import BaseModel
from typing import List

class BulkRandomRangeRequest(BaseModel):
    bulk: int
    max: int
    min: int

class BulkRandomRangeResult(BaseModel):
    success: bool
    generator: str
    numbers: List[int]