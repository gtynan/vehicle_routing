from typing import List, Optional
from datetime import datetime, timedelta

from src.models.base import BaseModel
from src.models.driver import Driver
from src.models.route import Route
from src.models.location import Location


class Schedule(BaseModel):
    driver: Driver
    route: List[Route]

    @staticmethod
    def from_raw(
        driver_id: int,
        route: List[int],
        time: List[int],
        locations: Optional[List[str]] = None,
    ) -> "Schedule":
        driver = Driver(id=driver_id)
        driver_route = [
            Route(
                id=i,
                start=Location(
                    name=locations[route[i]] if locations else str(route[i])
                ),  # pass name if given
                end=Location(
                    name=locations[route[i + 1]] if locations else str(route[i + 1])
                ),
                duration=time[i + 1] - time[i],
                arrival_time=(
                    datetime.now()
                    + timedelta(seconds=time[i + 1])
                    - timedelta(seconds=time[0])  # remove starting load from time calc
                ).time(),
            )
            for i in range(len(route) - 1)
        ]
        return Schedule(driver=driver, route=driver_route)
