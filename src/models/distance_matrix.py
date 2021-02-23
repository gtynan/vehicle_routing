from typing import List

from src.models.base import BaseModel


class DistanceMatrix(BaseModel):
    locations: List[str]
    driver_indicies: List[int]
    matrix: List[List[int]]
