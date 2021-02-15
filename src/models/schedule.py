from typing import Any, List, Optional

from src.models.base import BaseModel
from src.models.driver import Driver
from src.models.route import Route
from src.models.location import Location


class Schedule(BaseModel):
    driver: Driver
    route: List[Route]

    @staticmethod
    def from_raw(driver_id: int, route: List[int], distance_matrix: List[List[int]], locations: Optional[List[str]] = None) -> "Schedule":
        driver = Driver(id=driver_id)
        driver_route = [
            Route(id=i, 
                  start=Location(name=locations[route[i]] if locations else str(route[i])), # pass name if given
                  end=Location(name=locations[route[i+1]] if locations else str(route[i+1])),
                  duration=distance_matrix[route[i]][route[i+1]]) \
                  for i in range(len(route)-1)
        ]
        return Schedule(driver=driver, route=driver_route)
