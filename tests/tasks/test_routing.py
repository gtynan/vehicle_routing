from src.tasks.routing import get_routes


def test_traveling_salesman_get_routes(ts_distance_matrix):
    # [0] to get vehicle 0's route
    assert get_routes(ts_distance_matrix, 1, 0)[0] == [0, 7, 2, 3, 4, 12, 6, 8, 1, 11, 10, 5, 9, 0]


def test_multiple_vehicle_get_routes(mv_distance_matrix):
    assert get_routes(mv_distance_matrix, 4, 0) == [[0, 8, 6, 2, 5, 0], 
                                                    [0, 7, 1, 4, 3, 0], 
                                                    [0, 9, 10, 16, 14, 0], 
                                                    [0, 12, 11, 15, 13 , 0]]


def test_pickup_delivery_get_routes(mv_distance_matrix, pickup_deliver):
    # to get matching result to docs: https://developers.google.com/optimization/routing/pickup_delivery
    # must change paramms to: routing_enums_pb2.FirstSolutionStrategy.PARALLEL_CHEAPEST_INSERTION
    assert get_routes(mv_distance_matrix, 4, 0, pickup_deliver) == [[0, 16, 14, 13, 12, 0], 
                                                                    [0, 7, 1, 6, 8, 0], 
                                                                    [0, 4, 3, 15, 11, 0], 
                                                                    [0, 5, 2, 10, 9, 0]]
