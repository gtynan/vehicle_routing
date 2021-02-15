from typing import List
from fastapi import APIRouter
from starlette.status import HTTP_200_OK

from src.models.distance_matrix import DistanceMatrix
from src.tasks.distance_matrix import get_distance_matrix


router = APIRouter(prefix="/distance_matrix")


@router.post("/create", response_model=DistanceMatrix, name="distance_matrix:create", status_code=HTTP_200_OK)
def create_distance_matrix(
    locations: List[str],
) -> DistanceMatrix:
    """Create a distance matrix for the specified locations

    Args:
        locations (List[str]): location names

    Returns:
        DistanceMatrix: locations specified and corresponding distance matrix
    """
    matrix = get_distance_matrix(locations)
    return DistanceMatrix(locations=locations, matrix=matrix)
