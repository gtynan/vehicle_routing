from typing import List
from fastapi import APIRouter
from starlette.status import HTTP_200_OK

from src.models.distance_matrix import DistanceMatrix
from src.tasks.distance_matrix import get_distance_matrix


router = APIRouter(prefix="/distance_matrix")


@router.post(
    "/create",
    response_model=DistanceMatrix,
    name="distance_matrix:create",
    status_code=HTTP_200_OK,
)
def create_distance_matrix(
    return_home: bool, location_names: List[str], driver_indicies: List[int]
) -> DistanceMatrix:

    matrix = get_distance_matrix(
        location_names, driver_indicies, return_home=return_home
    )
    return DistanceMatrix(
        locations=location_names, driver_indicies=driver_indicies, matrix=matrix
    )
