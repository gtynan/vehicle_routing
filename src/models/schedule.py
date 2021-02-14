from typing import List
from src.models.base import BaseModel
from src.models.driver import Driver
from src.models.route import Route


class Schedule(BaseModel):
    driver: Driver
    routes: List[Route]
