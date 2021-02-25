from typing import List, Optional, Tuple
from ortools.constraint_solver import pywrapcp, routing_enums_pb2

# dimension names
TIME_DIMENSION = "Time"
CAPACITY_DIMENSION = "Capacity"

# default search params
SEARCH_PARAMS = pywrapcp.DefaultRoutingSearchParameters()
SEARCH_PARAMS.first_solution_strategy = (
    routing_enums_pb2.FirstSolutionStrategy.PATH_CHEAPEST_ARC
)
SEARCH_PARAMS.time_limit.seconds = 10  # Timeout if solution not found


class Router:
    def __init__(
        self, params: pywrapcp.DefaultRoutingSearchParameters = SEARCH_PARAMS
    ) -> None:
        self.params = params

    def solve(
        self,
        time_matrix: List[List[int]],
        driver_indicies: List[int],
        delivery_pairs: List[Tuple[int]],
        delivery_weights: Optional[List[int]] = None,
        vehicle_capacities: Optional[List[int]] = None,
        site_eta: Optional[List[int]] = None,
        time_worked: Optional[List[int]] = None,
        max_time: int = 28800,
    ) -> None:
        """Attempt to find a solution within the given constraints, will raise exception if fails"""
        n_locations, n_vehicles = len(time_matrix), len(driver_indicies)

        # ensure all inputs correct
        _check_inputs(
            n_locations,
            n_vehicles,
            vehicle_capacities,
            site_eta,
            delivery_weights,
            delivery_pairs,
            time_worked,
        )

        # depot nodes act as start and end positions
        self.manager = pywrapcp.RoutingIndexManager(
            n_locations, n_vehicles, driver_indicies, driver_indicies
        )
        self.routing = pywrapcp.RoutingModel(self.manager)

        self._add_time_dimension(time_matrix, max_time, site_eta, time_worked)
        self._add_delivery_constraint(delivery_pairs)

        # only add capacity constraint if needed
        if delivery_weights and vehicle_capacities:
            self._add_capacity_dimension(
                n_locations,
                delivery_weights,
                delivery_pairs,
                vehicle_capacities,
                driver_indicies,
            )

        self.solution = self.routing.SolveWithParameters(self.params)
        if self.solution is None:
            raise Exception("Solution not found")

    def get_route_list(self):
        """Get list of routes for each driver, locations are given as indicies relating to their position in the time matrix"""
        routes = []
        for vehicle_id in range(self.manager.GetNumberOfVehicles()):
            # starting index
            index = self.routing.Start(vehicle_id)
            # overall route for this specific vehicle
            route = [self.manager.IndexToNode(index)]

            # append to route while not at final indedx
            while not self.routing.IsEnd(index):
                # next index to visit
                index = self.solution.Value(self.routing.NextVar(index))
                route.append(self.manager.IndexToNode(index))
            routes.append(route)
        return routes

    def get_route_times(self):
        """Get expected duration of each route, value represents duration already incurred + current duration"""
        time_dimension = self.routing.GetDimensionOrDie(TIME_DIMENSION)
        times = []
        for vehicle_id in range(self.manager.GetNumberOfVehicles()):
            index = self.routing.Start(vehicle_id)
            vehicle_time = []
            while not self.routing.IsEnd(index):
                vehicle_time.append(self.solution.Min(time_dimension.CumulVar(index)))
                index = self.solution.Value(self.routing.NextVar(index))

            vehicle_time.append(self.solution.Min(time_dimension.CumulVar(index)))
            times.append(vehicle_time)
        return times

    def _add_time_dimension(
        self,
        time_matrix: List[List[int]],
        max_time: int,
        site_eta: Optional[List[int]] = None,
        time_worked: Optional[List[int]] = None,
    ) -> None:
        def time_callback(from_index: int, to_index: int) -> float:
            """Calculates time between two indicies"""
            from_node = self.manager.IndexToNode(from_index)
            to_node = self.manager.IndexToNode(to_index)

            travel_time = time_matrix[from_node][to_node]
            if site_eta:
                travel_time += site_eta[from_node]
            return travel_time

        transit_callback_index = self.routing.RegisterTransitCallback(time_callback)

        # setting cost as time (routing will attempt to minimise this cost)
        self.routing.SetArcCostEvaluatorOfAllVehicles(transit_callback_index)

        self.routing.AddDimension(
            transit_callback_index,
            0,  # no slack
            max_time,  # maximum time per vehicle
            False,  # Don't force start cumul to zero.
            TIME_DIMENSION,
        )

        time_dimension = self.routing.GetDimensionOrDie(TIME_DIMENSION)

        # force each vehicle to start at time 0 otherwise optimiser will adjust start times to minimise overall diff between lowest start and biggest end
        for vehicle_id in range(self.manager.GetNumberOfVehicles()):
            index = self.routing.Start(vehicle_id)
            # we can specify how long already certain drivers have worked
            starting_value = time_worked[vehicle_id] if time_worked else 0
            time_dimension.CumulVar(index).SetValue(starting_value)

        # minimises: coefficient * (Max(dimension end value) - Min(dimension start value)).
        time_dimension.SetGlobalSpanCostCoefficient(100)

        return time_dimension

    def _add_delivery_constraint(
        self,
        pickup_delivery_data: List[List[int]],
    ) -> None:
        time_dimension = self.routing.GetDimensionOrDie(TIME_DIMENSION)

        # set rules for pickup and delivery relationships
        for pickup_node, delivery_node in pickup_delivery_data:

            # all nodes are automatically visted so only set a delivery constraint if required
            if pickup_node != delivery_node:

                pickup_index = self.manager.NodeToIndex(pickup_node)
                delivery_index = self.manager.NodeToIndex(delivery_node)

                # pick up delivery request
                self.routing.AddPickupAndDelivery(pickup_index, delivery_index)

                # same vehicle must both pick up and deliver
                self.routing.solver().Add(
                    self.routing.VehicleVar(pickup_index)
                    == self.routing.VehicleVar(delivery_index)
                )

                # contraint pickup must occur before delivery
                self.routing.solver().Add(
                    time_dimension.CumulVar(pickup_index)
                    <= time_dimension.CumulVar(delivery_index)
                )

                # constraint pickup vehicle must go straight to delivery
                self.routing.solver().Add(
                    self.routing.NextVar(pickup_index) == delivery_index
                )

    def _add_capacity_dimension(
        self,
        n_locations: int,
        requirements: List[int],
        delivery_pairs: List[int],
        capacities: List[int],
        driver_indicies: List[int],
    ) -> None:
        def demand_callback(from_index):
            """Returns the demand of the node."""

            def get_flat_requirements():
                """Flat list of weight requirements for each node"""
                reqs = [0] * n_locations
                for req, (pickup, delivery) in zip(requirements, delivery_pairs):
                    if pickup != delivery:
                        reqs[pickup] = req
                        reqs[delivery] = -req
                return reqs

            from_node = self.manager.IndexToNode(from_index)
            if from_node in driver_indicies:
                # nothing is carried from depots
                return 0
            return get_flat_requirements()[from_node]

        demand_callback_index = self.routing.RegisterUnaryTransitCallback(
            demand_callback
        )

        self.routing.AddDimensionWithVehicleCapacity(
            demand_callback_index,
            0,  # null capacity slack
            capacities,  # vehicle maximum capacities
            True,  # start cumul to zero
            CAPACITY_DIMENSION,
        )


def _check_inputs(
    n_locations,
    n_vehicles,
    vehicle_capacities,
    site_eta,
    delivery_weights,
    delivery_pairs,
    time_worked,
) -> None:
    """Ensure all inputs correct"""
    try:
        assert n_vehicles > 0
    except:
        raise Exception("Must have at least 1 depot node")
    try:
        assert n_locations > 1
    except:
        raise Exception("Must have at least 2 locations")
    if vehicle_capacities:
        try:
            assert n_vehicles == len(vehicle_capacities)
        except:
            raise Exception(
                "len(vehicle_capacities) != len(depot_nodes), require capacity for each vehicle"
            )
    if site_eta:
        try:
            assert n_locations == len(site_eta)
        except:
            raise Exception(
                "len(time_matrix) != len(site_eta), require site eta for all locations"
            )

    if delivery_weights:
        try:
            assert len(delivery_weights) == len(delivery_pairs)
        except:
            raise Exception(
                "len(delivery_weights) != len(delivery_pairs), require delivery weights for all delivery pairs"
            )

    if time_worked:
        try:
            assert len(time_worked) == n_vehicles
        except:
            raise Exception(
                "len(time_worked) != len(depot_nodes), require time worked for all vehicles"
            )
