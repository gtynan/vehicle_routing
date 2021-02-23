import logging
from typing import List
from fastapi import APIRouter
from starlette.status import HTTP_200_OK

from src.models.distance_matrix import DistanceMatrix
from src.tasks.distance_matrix import get_distance_matrix


# get root logger
logger = logging.getLogger(__name__)


router = APIRouter(prefix="/distance_matrix")


@router.post(
    "/create",
    response_model=DistanceMatrix,
    name="distance_matrix:create",
    status_code=HTTP_200_OK,
)
def create_distance_matrix(
    return_home: bool, location_names: List[str], depot_nodes: List[int]
) -> DistanceMatrix:
    logger.info("create schedule")

    matrix = get_distance_matrix(location_names, depot_nodes, return_home=return_home)
    return DistanceMatrix(
        locations=location_names, driver_indicies=depot_nodes, matrix=matrix
    )
