import logging
from typing import List, Optional, Tuple
from fastapi import APIRouter, HTTPException, Depends
from starlette.status import HTTP_200_OK

from src.models.schedule import Schedule
from src.tasks.routing import Router


logger = logging.getLogger(__name__)


router = APIRouter(prefix="/schedule")


def routing_model() -> Router:
    return Router()


@router.post(
    "/create",
    response_model=List[Schedule],
    name="schedule:create",
    status_code=HTTP_200_OK,
)
def create_schedule(
    time_matrix: List[List[int]],
    driver_indicies: List[int],
    delivery_pairs: List[Tuple[int, int]],
    delivery_weights: Optional[List[int]] = None,
    vehicle_capacities: Optional[List[int]] = None,
    site_eta: Optional[List[int]] = None,
    time_worked: Optional[List[int]] = None,
    max_time: int = 28800,
    location_names: Optional[List[str]] = None,
    routing_model: Router = Depends(routing_model),
) -> List[Schedule]:
    """Create a schedule for each driver within the given constraints

    Args:
        max_time (int): Max time any one driver can work
        time_matrix (List[List[int]]): matrix representation of the distances between each location
        driver_indicies (List[int]): indicies where locations relate to a drivers location
        delivery_pairs (List[Tuple[int, int]]): (pickup index, delivery index) for each delivery. If not delivering give same pickup and delivery index
        delivery_weights (Optional[List[int]]): vehicle capacity required to fulfill delivery.
        vehicle_capacities (Optional[List[int]]): max capacity for each vehicle
        site_eta (Optional[List[int]]): estimated time at each location
        time_worked (Optional[List[int]]): time already worked by each driver before this reques to ensure dont exceed max time
        location_names (Optional[List[str]]): Names of locations in the time matrix

    Returns:
        List[Schedule]: Schedule for each driver
    """

    # log all inputs
    logger.info(
        f"""Inputs:
        time_matrix: {time_matrix}, 
        driver_indicies: {driver_indicies}, 
        delivery_pairs: {delivery_pairs}, 
        delivery_weights: {delivery_weights}, 
        vehicle_capacities: {vehicle_capacities}, 
        site_eta: {site_eta}, 
        time_worked: {time_worked}
        max_time: {max_time}
        location_names: {location_names}"""
    )

    try:
        routing_model.solve(
            time_matrix=time_matrix,
            driver_indicies=driver_indicies,
            delivery_pairs=delivery_pairs,
            delivery_weights=delivery_weights,
            vehicle_capacities=vehicle_capacities,
            site_eta=site_eta,
            time_worked=time_worked,
            max_time=max_time,
        )
        # list of schedules, 1 for each driver
        return [
            Schedule.from_raw(
                driver_id=i,
                route=routes,
                time=times,
                locations=location_names,
            )
            for i, (routes, times) in enumerate(
                zip(routing_model.get_route_list(), routing_model.get_route_times())
            )
        ]
    except Exception as e:
        logger.error(str(e))
        raise HTTPException(
            status_code=422,
            detail=str(e),
        )
