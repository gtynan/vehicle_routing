from typing import List, Optional
from fastapi import APIRouter

from src.models.schedule import Schedule
from src.tasks.routing import get_routes
from src.tasks.convert import route_list_to_model


router = APIRouter(prefix="/routes")


@router.post("/create_schedule", response_model=List[Schedule], name="routes:create_schedule")
def create_schedule(
    n_vehicles: int,
    depot_node: int,
    distance_matrix: List[List[int]],
    pickup_delivery: Optional[List[List[int]]] = None
) -> List[Schedule]:
    routes = get_routes(n_vehicles=n_vehicles, depot_node=depot_node, distance_matrix=distance_matrix, pickup_delivery_data=pickup_delivery)
    return route_list_to_model(routes)
