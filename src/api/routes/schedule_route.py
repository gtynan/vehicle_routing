from typing import List, Optional, Tuple
from fastapi import APIRouter, HTTPException, Depends
from starlette.status import HTTP_200_OK

from src.models.schedule import Schedule
from src.tasks.routing import Router


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
    depot_nodes: List[int],
    delivery_pairs: List[Tuple[int, int]],
    delivery_weights: Optional[List[int]] = None,
    vehicle_capacities: Optional[List[int]] = None,
    site_eta: Optional[List[int]] = None,
    time_worked: Optional[List[int]] = None,
    max_time: int = 28800,
    location_names: Optional[List[str]] = None,
    routing_model: Router = Depends(routing_model),
) -> List[Schedule]:

    try:
        routing_model.solve(
            time_matrix=time_matrix,
            depot_nodes=depot_nodes,
            delivery_pairs=delivery_pairs,
            delivery_weights=delivery_weights,
            vehicle_capacities=vehicle_capacities,
            site_eta=site_eta,
            time_worked=time_worked,
            max_time=max_time,
        )
        print(routing_model)
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
    except:
        raise HTTPException(
            status_code=422,
            detail="Could not converge on optimal route within specified constraints",
        )
