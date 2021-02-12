from src.routing import get_routes


def test_traveling_salesman_get_routes(ts_distance_matrix):
    # [0] to get vehicle 0's route
    assert get_routes(ts_distance_matrix, 1, 0)[0] == [0, 7, 2, 3, 4, 12, 6, 8, 1, 11, 10, 5, 9, 0]


def test_multiple_vehicle_get_routes(mv_distance_matrix):
    assert get_routes(mv_distance_matrix, 4, 0) == [[0, 8, 6, 2, 5, 0], 
                                                    [0, 7, 1, 4, 3, 0], 
                                                    [0, 9, 10, 16, 14, 0], 
                                                    [0, 12, 11, 15, 13 , 0]]
