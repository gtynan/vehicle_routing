import logging
from typing import List
from fastapi import APIRouter
from starlette.status import HTTP_200_OK

from src.models.time_matrix import TimeMatrix
from src.tasks.time_matrix import get_time_matrix


# get root logger
logger = logging.getLogger(__name__)


router = APIRouter(prefix="/time_matrix")


@router.post(
    "/create",
    response_model=TimeMatrix,
    name="time_matrix:create",
    status_code=HTTP_200_OK,
)
def create_time_matrix(
    return_home: bool, locations: List[str], driver_indicies: List[int]
) -> TimeMatrix:
    """Create a time matrix to represent distance between locations

    Args:
        locations (List[str]): Names of locations of interest
        driver_indicies (List[int]): indicies where locations relate to a drivers location
        return_home: Whether or not to include returning to home as a distance.

    Returns:
        TimeMatrix
    """

    logging.info(
        f"""INPUTS:
    locations: {locations},
    driver_indicies: {driver_indicies},
    return_home: {return_home}"""
    )

    matrix = get_time_matrix(locations, driver_indicies, return_home)
    return TimeMatrix(nodes=locations, driver_indicies=driver_indicies, matrix=matrix)
