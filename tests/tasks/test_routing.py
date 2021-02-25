import pytest
import numpy as np
from ortools.constraint_solver import pywrapcp, routing_enums_pb2

from src.tasks.routing import Router


class TestRouter:
    def test_solve_basic(self, mv_distance_matrix, pickup_deliver):
        # Ensure matches google docs
        # SOURCE: https://developers.google.com/optimization/routing/pickup_delivery
        expected_routes = [
            [0, 13, 15, 11, 12, 0],
            [0, 5, 2, 10, 16, 14, 9, 0],
            [0, 4, 3, 0],
            [0, 7, 1, 6, 8, 0],
        ]

        params = pywrapcp.DefaultRoutingSearchParameters()
        params.first_solution_strategy = (
            routing_enums_pb2.FirstSolutionStrategy.PARALLEL_CHEAPEST_INSERTION
        )

        router = Router(params)
        router.solve(
            time_matrix=mv_distance_matrix,
            driver_indicies=[0] * 4,  # all drivers depart from node 0
            delivery_pairs=pickup_deliver,
        )
        router.get_route_list() == expected_routes

        # cannot solve when max time = 0
        with pytest.raises(Exception):
            router.solve(
                time_matrix=mv_distance_matrix,
                delivery_pairs=pickup_deliver,
                driver_indicies=[0] * 4,
                max_time=0,
            )

    def test_solve_with_capacity_constraints(self, mv_distance_matrix):
        # make matrix smaller(7*7)
        matrix = np.array(mv_distance_matrix)[:7, :7]

        router = Router()
        router.solve(
            time_matrix=matrix,
            driver_indicies=[0] * 3,
            delivery_pairs=[(1, 2), (3, 4), (5, 6)],
            delivery_weights=[1, 2, 2],
            vehicle_capacities=[0, 1, 2],
        )
        routes = np.array(router.get_route_list())
        # vehicle 0 has no capacity and all deliveries require capacity so shouldn't leave depot
        assert np.isin(routes[0], [0]).all()
        # vehicle 1 has capacity = 1 only 1 delivery matches that
        assert np.isin(routes[1], [0, 1, 2]).all()
        # vehicle 2 gets remaining deliveries
        assert np.isin(routes[2], [0, 3, 4, 5, 6]).all()

    def test_solve_with_different_starting_nodes(self, mv_distance_matrix):
        # make matrix smaller(9*9)
        matrix = np.array(mv_distance_matrix)[:9, :9]

        router = Router()
        router.solve(
            time_matrix=matrix,
            driver_indicies=[0, 7, 8],
            delivery_pairs=[(1, 2), (3, 4), (5, 6)],
            delivery_weights=[2] * 3,
            vehicle_capacities=[2] * 3,
        )
        routes = np.array(router.get_route_list())
        # ensure routes starting nodes match expected
        np.testing.assert_array_equal(routes[:, 0], [0, 7, 8])
        # ensure routes ending nodes match expected
        np.testing.assert_array_equal(routes[:, -1], [0, 7, 8])

    def test_solve_with_starting_time(self, mv_distance_matrix):
        # make matrix smaller(5*5)
        matrix = np.array(mv_distance_matrix)[:6, :6]

        router = Router()
        router.solve(
            time_matrix=matrix,
            driver_indicies=[0, 5],
            delivery_pairs=[(1, 2), (3, 4)],
            site_eta=[20000, 0, 0, 0, 0, 0],
        )
        times = np.array(router.get_route_times())

        # all routes should be assigned to vehicle 1
        # as vehicle 0 has long starting delay
        assert len(times[0]) == 2
        assert times[0][1] == 20000

    def test_solve_with_time_worked(self, mv_distance_matrix):
        # make matrix smaller(5*5)
        matrix = np.array(mv_distance_matrix)[:6, :6]

        router = Router()
        router.solve(
            time_matrix=matrix,
            driver_indicies=[0, 5],
            delivery_pairs=[(1, 2), (3, 4)],
            time_worked=[20000, 0],
            max_time=20000,
        )
        times = np.array(router.get_route_times())
        routes = np.array(router.get_route_list())

        # driver 0 has already worked max time ensure no routes scheduled
        assert len(routes[0]) == 2
        assert routes[0][0] == routes[0][1] == 0  # ensure never leaves depot
        assert len(times[0]) == 2  # two as start and end
        assert times[0][0] == times[0][1] == 20000
