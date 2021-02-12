from typing import List
from ortools.constraint_solver import pywrapcp, routing_enums_pb2
import numpy as np

search_parameters = pywrapcp.DefaultRoutingSearchParameters()
search_parameters.first_solution_strategy = (
    routing_enums_pb2.FirstSolutionStrategy.PATH_CHEAPEST_ARC)


def _create_routing_manager(distance_matrix: np.ndarray, n_vehicles: int, depot_node: int):
    return pywrapcp.RoutingIndexManager(len(distance_matrix), n_vehicles, depot_node)


def _create_routing_model(distance_matrix: np.ndarray, manager: pywrapcp.RoutingIndexManager) -> pywrapcp.RoutingModel:
    def distance_callback(from_index: int, to_index: int) -> float:
        """Calculates distance between two indicies
        """
        from_node = manager.IndexToNode(from_index)
        to_node = manager.IndexToNode(to_index)
        return distance_matrix[from_node][to_node]

    routing = pywrapcp.RoutingModel(manager)
    transit_callback_index = routing.RegisterTransitCallback(distance_callback)
    
    # setting cost as distance (routing will attempt to minimise this cost)
    routing.SetArcCostEvaluatorOfAllVehicles(transit_callback_index)
    return routing


def get_routes(distance_matrix: np.ndarray, n_vehicles: int, depot_node: int, params: pywrapcp.DefaultRoutingSearchParameters = search_parameters) -> List[int]:
    """Create optimal route path in a 2 dimensional array. Value i, j refers to vehicles i's jth location to visit

    Args:
        distance_matrix (np.ndarray): Distances between all locations
        n_vehicles (int): Number of vehicles available
        depot_node (int): Starting node
        params (pywrapcp.DefaultRoutingSearchParameters, optional): [description]. Defaults to search_parameters.

    Returns:
        List[int]: 2 dimensional array of routes for each vehicle
    """
    manager = _create_routing_manager(distance_matrix, n_vehicles, depot_node)
    model = _create_routing_model(distance_matrix, manager)

    solution = model.SolveWithParameters(params)

    routes = []
    for route_nbr in range(model.vehicles()):
        # starting index
        index = model.Start(route_nbr)
        # overall route for this specific vehicle
        route = [manager.IndexToNode(index)]

        # append to route while not at final indedx
        while not model.IsEnd(index):
            # next index to visit
            index = solution.Value(model.NextVar(index))
            route.append(manager.IndexToNode(index))
        routes.append(route)

    return routes
