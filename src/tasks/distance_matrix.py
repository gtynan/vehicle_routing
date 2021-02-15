from typing import List
import requests

from src.core.config import API_KEY, API_ADDRESS
from src.models.distance_matrix import DistanceMatrix


# Distance Matrix API only accepts 100 elements per request.
MAX_ELEMENTS = 100


def get_distance_matrix(locations: List[str]) -> List[List[int]]:
    """Create a distance matrix given a list of locations

    Args:
        locations (List[str]): location names

    Returns:
        List[List[int]]: distance matrix
    """
    n_locations = len(locations)
    # max rows per request such that max elements not exceeded
    max_rows = MAX_ELEMENTS // n_locations

    # n full requests (MAX ELEMENTS achieved)
    n_full, n_remaining = divmod(n_locations, max_rows)
    distance_matrix = []

    for i in range(n_full):
        origin_addresses = locations[i * max_rows: (i + 1) * max_rows]
        response = _send_request(origin_addresses, locations)
        distance_matrix += _build_distance_matrix(response)
    
    # Get the remaining remaining n_remaining rows, if necessary.
    if n_remaining > 0:
        origin_addresses = locations[n_full * max_rows: n_full * max_rows + n_remaining]
        response = _send_request(origin_addresses, locations)
        distance_matrix += _build_distance_matrix(response)
    return distance_matrix


def _send_request(origin_addresses, dest_addresses):
    """Build and send request for the given origin and destination addresses.
    """
    def build_address_str(addresses):
        return "|".join(addresses) # Build a pipe-separated string of addresses

    origin_address_str = build_address_str(origin_addresses)
    dest_address_str = build_address_str(dest_addresses)

    # API request
    res = requests.get(
        API_ADDRESS,
        params = {
            "units": "imperial", # response in english
            "origins": origin_address_str,
            "destinations": dest_address_str,
            "key": API_KEY
        }
    )
    return res.json()


def _build_distance_matrix(res_json):
    """Create distance matrix from json
    """
    distance_matrix = []
    for row in res_json['rows']:
        # distance can also be duration to handle time
        row_list = [row['elements'][j]['duration']['value'] for j in range(len(row['elements']))]
        distance_matrix.append(row_list)
    return distance_matrix
