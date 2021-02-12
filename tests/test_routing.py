from src.routing import get_routes


def test_get_routes(distance_matrix):
    # [0] to get vehicle 0's route
    assert get_routes(distance_matrix, 1, 0)[0] == [0, 7, 2, 3, 4, 12, 6, 8, 1, 11, 10, 5, 9, 0]
