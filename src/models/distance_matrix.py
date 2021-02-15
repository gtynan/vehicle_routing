from typing import List

from src.models.base import BaseModel


class DistanceMatrix(BaseModel):
    locations: List[str]
    matrix: List[List[int]]
