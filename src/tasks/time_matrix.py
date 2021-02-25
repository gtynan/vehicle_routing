from typing import Any, List
import requests
import numpy as np

from src.core.config import API_KEY, API_ADDRESS


# Distance Matrix API only accepts 100 elements per request.
MAX_ELEMENTS = 100


def get_time_matrix(
    locations: List[str], driver_indicies: List[int], return_home: bool = True
) -> List[List[int]]:
    """Create a time matrix to represent distance between locations

    Args:
        locations (List[str]): Names of locations of interest
        driver_indicies (List[int]): indicies of locations that relate to a driver
        return_home (bool, optional): Whether or not to include returning to home as a distance. Defaults to True.

    Returns:
        List[List[int]]: Time matrix
    """
    n_locations = len(locations)
    # max rows per request such that max elements not exceeded
    max_rows = MAX_ELEMENTS // n_locations

    # n full requests (MAX ELEMENTS achieved)
    n_full, n_remaining = divmod(n_locations, max_rows)
    distance_matrix = []

    for i in range(n_full):
        origin_addresses = locations[i * max_rows : (i + 1) * max_rows]
        response = _send_request(origin_addresses, locations)
        distance_matrix += _build_distance_matrix(response)

    # Get the remaining remaining n_remaining rows, if necessary.
    if n_remaining > 0:
        origin_addresses = locations[
            n_full * max_rows : n_full * max_rows + n_remaining
        ]
        response = _send_request(origin_addresses, locations)
        distance_matrix += _build_distance_matrix(response)

    if not return_home:
        distance_matrix = np.array(distance_matrix)
        # all routes to starting driver locations given time of 0 so that not counted
        distance_matrix[:, driver_indicies] = 0
        distance_matrix = distance_matrix.tolist()

    return distance_matrix


def _send_request(
    origin_addresses: List[Any], dest_addresses: List[Any], coordinates: bool = False
) -> dict:
    """Build and send request for the given origin and destination addresses.

    Args:
        origin_addresses (List[Any]): Can be str addresses or tuples of coordinates
        dest_addresses (List[Any]): Can be str addresses or tuples of coordinates
        coordinates (bool): flags whether lat long tuples passed or address strings

    Returns:
        dict: request json data
    """

    def build_address_str(addresses):
        return "|".join(addresses)  # Build a pipe-separated string of addresses

    def build_coord_str(addresses):
        # must pre format if latitude and long such that each entry = "lat, long"
        return build_address_str([f"{lat}, {lon}" for lat, lon in addresses])

    origin_address_str = (
        build_coord_str(origin_addresses)
        if coordinates
        else build_address_str(origin_addresses)
    )
    dest_address_str = (
        build_coord_str(dest_addresses)
        if coordinates
        else build_address_str(dest_addresses)
    )

    # API request
    res = requests.get(
        API_ADDRESS,
        params={
            "units": "imperial",  # response in english
            "origins": origin_address_str,
            "destinations": dest_address_str,
            "key": API_KEY,
        },
    )
    return res.json()


def _build_distance_matrix(
    res_json: dict, measure: str = "duration"
) -> List[List[int]]:
    """Create distance matrix from json

    Args:
        measure (str): Either duration or distance. Defaults to duration

    Returns:
        List[List[int]]: Distance matrix
    """
    # only two allowed measures
    assert measure in ["distance", "duration"]

    distance_matrix = []
    for row in res_json["rows"]:
        row_list = [
            row["elements"][j][measure]["value"] for j in range(len(row["elements"]))
        ]
        distance_matrix.append(row_list)

    return distance_matrix
