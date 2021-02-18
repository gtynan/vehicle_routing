from typing import List, Optional
from ortools.constraint_solver import pywrapcp, routing_enums_pb2


# default search params
SEARCH_PARAMS = pywrapcp.DefaultRoutingSearchParameters()
SEARCH_PARAMS.first_solution_strategy = (
    routing_enums_pb2.FirstSolutionStrategy.PATH_CHEAPEST_ARC)
# Timeout if solution not found
SEARCH_PARAMS.time_limit.seconds = 10


def _create_routing_manager(n_locations: int, n_vehicles: int, depot_node: int):
    return pywrapcp.RoutingIndexManager(n_locations, n_vehicles, depot_node)


def _create_routing_model(distance_matrix: List[List[int]], 
                          manager: pywrapcp.RoutingIndexManager, 
                          pickup_delivery_data: Optional[List] = None, 
                          max_distance: Optional[int] = None) -> pywrapcp.RoutingModel:
   
    def distance_callback(from_index: int, to_index: int) -> float:
        """Calculates distance between two indicies
        """
        from_node = manager.IndexToNode(from_index)
        to_node = manager.IndexToNode(to_index)
        return distance_matrix[from_node][to_node]

    # must specify max distance if more than 1 vehicle
    distance_constraint = manager.GetNumberOfVehicles() > 1
    if distance_constraint:
        assert isinstance(max_distance, int)

    routing = pywrapcp.RoutingModel(manager)
    transit_callback_index = routing.RegisterTransitCallback(distance_callback)
    
    # setting cost as distance (routing will attempt to minimise this cost)
    routing.SetArcCostEvaluatorOfAllVehicles(transit_callback_index)
    
    # Add Distance constraint.
    if distance_constraint:
        dimension_name = 'Distance'
        routing.AddDimension(
            transit_callback_index,
            0,  # No slack
            max_distance,
            True,  # start cumul to zero
            dimension_name)
        distance_dimension = routing.GetDimensionOrDie(dimension_name)
        distance_dimension.SetGlobalSpanCostCoefficient(100)

    # create pickup and delivery relationships
    if pickup_delivery_data and distance_constraint:
        for request in pickup_delivery_data:
            pickup_index = manager.NodeToIndex(request[0])
            delivery_index = manager.NodeToIndex(request[1])
            # pick up delievry request
            routing.AddPickupAndDelivery(pickup_index, delivery_index)
            # constrain that same vehicle must both pick up and deliver
            routing.solver().Add(
                routing.VehicleVar(pickup_index) == routing.VehicleVar(
                    delivery_index))
            # contraint pickup must occur before delivery
            routing.solver().Add(
                distance_dimension.CumulVar(pickup_index) <=
                distance_dimension.CumulVar(delivery_index))

    return routing


def get_routes(distance_matrix: List[List[int]], 
               n_vehicles: int, 
               depot_node: int, 
               pickup_delivery_data: Optional[List] = None, 
               max_distance: int = 28800,
               params: pywrapcp.DefaultRoutingSearchParameters = SEARCH_PARAMS) -> List[int]:
    """Create optimal route path in a 2 dimensional array. Value i, j refers to vehicles i's jth location to visit

    Args:
        distance_matrix (np.ndarray): Distances between all locations
        n_vehicles (int): Number of vehicles available
        depot_node (int): Starting node
        params (pywrapcp.DefaultRoutingSearchParameters, optional): [description]. Defaults to search_parameters.

    Returns:
        List[int]: 2 dimensional array of routes for each vehicle
    """
    manager = _create_routing_manager(len(distance_matrix), n_vehicles, depot_node)
    model = _create_routing_model(distance_matrix, manager, pickup_delivery_data=pickup_delivery_data, max_distance=max_distance) # add distance dimension if more than 1 vehicle
    solution = model.SolveWithParameters(params)

    # create route if optimal solution found
    if solution:
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
