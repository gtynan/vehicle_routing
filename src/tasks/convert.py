from typing import List

from src.models.schedule import Schedule
from src.models.driver import Driver
from src.models.route import Route
from src.models.location import Location


def route_list_to_model(routes: List[int]) -> List[Schedule]:
    schedule = []
    # each row is a route for a specific driver
    for i, route in enumerate(routes):
        driver = Driver(name=str(i))
        driver_routes = [
            Route(id = x, 
                  start = Location(name=str(route[x])), 
                  end = Location(name=str(route[x + 1]))) \
                      for x in range(len(route) - 1)]

        schedule.append(Schedule(driver=driver, routes=driver_routes))

    return schedule
