from typing import List, Optional
from fastapi import APIRouter, HTTPException
from starlette.status import HTTP_200_OK

from src.models.schedule import Schedule
from src.tasks.routing import get_routes


router = APIRouter(prefix="/schedule")


@router.post("/create", response_model=List[Schedule], name="schedule:create", status_code=HTTP_200_OK)
def create_schedule(
    n_vehicles: int,
    depot_node: int,
    distance_matrix: List[List[int]],
    pickup_delivery: Optional[List[List[int]]] = None,
    location_names: Optional[List[str]] = None
) -> List[Schedule]:
    """Create driver schedules for the following pickup an delivery requirements 

    Args:
        n_vehicles (int): Number of drivers
        depot_node (int): Starting point
        distance_matrix (List[List[int]]
        pickup_delivery (Optional[List[List[int]]], optional): Pickup and delivery pairs. Defaults to None.
        location_names (Optional[List[str]], optional): Name of locations in the matrix. Defaults to None

    Returns:
        List[Schedule]: Driving schedule for each driver
    """
    routes = get_routes(n_vehicles=n_vehicles, depot_node=depot_node, distance_matrix=distance_matrix, pickup_delivery_data=pickup_delivery)
    if routes is None:
        raise HTTPException(status_code=422, detail="Could not converge on optimal route within specified constraints")
    print(location_names)
    return [Schedule.from_raw(driver_id=i, 
                              route=routes[i], 
                              distance_matrix=distance_matrix, 
                              locations=location_names) for i in range(len(routes))]
