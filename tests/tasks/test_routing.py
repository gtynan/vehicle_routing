from typing import List
import pytest
from ortools.constraint_solver import pywrapcp, routing_enums_pb2

from src.tasks.routing import get_routes


def test_traveling_salesman_get_routes(ts_distance_matrix):
    # Ensure matches google docs
    # SOURCE: https://developers.google.com/optimization/routing/tsp
    expected_routes = [[0, 7, 2, 3, 4, 12, 6, 8, 1, 11, 10, 5, 9, 0]]
    assert get_routes(ts_distance_matrix, 1, 0) == expected_routes


def test_multiple_vehicle_get_routes(mv_distance_matrix):
    # Ensure matches google docs
    # SOURCE: https://developers.google.com/optimization/routing/vrp
    expected_routes = [[0, 8, 6, 2, 5, 0], 
                        [0, 7, 1, 4, 3, 0], 
                        [0, 9, 10, 16, 14, 0], 
                        [0, 12, 11, 15, 13, 0]]
    params = pywrapcp.DefaultRoutingSearchParameters()
    params.first_solution_strategy = (routing_enums_pb2.FirstSolutionStrategy.PATH_CHEAPEST_ARC)
    assert get_routes(mv_distance_matrix, 4, 0, max_distance=3000, params=params) == expected_routes


def test_pickup_delivery_get_routes(mv_distance_matrix, pickup_deliver):
    # Ensure matches google docs
    # SOURCE: https://developers.google.com/optimization/routing/pickup_delivery
    expected_routes = [[0, 13, 15, 11, 12, 0], 
                        [0, 5, 2, 10, 16, 14, 9, 0], 
                        [0, 4, 3, 0], 
                        [0, 7, 1, 6, 8, 0]]
    params = pywrapcp.DefaultRoutingSearchParameters()
    params.first_solution_strategy = (routing_enums_pb2.FirstSolutionStrategy.PARALLEL_CHEAPEST_INSERTION)
    assert get_routes(mv_distance_matrix, 4, 0, pickup_delivery_data=pickup_deliver, max_distance=3000, params=params) == expected_routes
