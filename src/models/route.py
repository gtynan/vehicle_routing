from datetime import time

from src.models.base import BaseModel
from src.models.location import Location


class Route(BaseModel):
    id: int
    start: Location
    end: Location
    duration: int
    arrival_time: time
