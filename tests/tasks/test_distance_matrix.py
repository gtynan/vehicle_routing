import pytest

from src.tasks.distance_matrix import get_distance_matrix, _build_distance_matrix, _send_request


@pytest.fixture(scope='module')
def dummy_locations():
    # str and coord addresses for same places
    return [
        'Cartow Vehicle Serivce, Finglas North, Dublin, Ireland', 
        'Island Upper, County Wexford, Y25 A344, Ireland'
    ], [
        (53.39868, -6.29710),
        (52.67862, -6.39381)
    ]

def test_get_distance_matrix(dummy_locations):
    matrix = get_distance_matrix(dummy_locations[0])
    n = len(matrix)
    assert n == len(dummy_locations[0])

    for i in range(n):
        for j in range(n):
            if i == j:
                assert matrix[i][j] == 0 # diagonal should always be 0 
            else:
                assert matrix[i][j] > 0


def test_send_request(dummy_locations):
    location_response = _send_request(dummy_locations[0], dummy_locations[0], coordinates=False)
    location_response = _build_distance_matrix(location_response, measure="duration")

    coord_response = _send_request(dummy_locations[1], dummy_locations[1], coordinates=True)
    coord_response = _build_distance_matrix(coord_response, measure="duration")

    # if measure used was distance would fail due to slight diff in coord vs locations
    assert location_response == coord_response


def test_build_distance_matrix():
    # dummy json that matches whats expected from google
    dummy_json = {
        "rows": [
            {
                "elements": [
                    {
                        "distance": {"value": 0},
                        "duration": {"value": 0}
                    },
                    {
                        "distance": {"value": 10},
                        "duration": {"value": 20}
                    }
                ]
            },
            {
                "elements": [
                    {
                        "distance": {"value": 10},
                        "duration": {"value": 20}
                    },
                    {
                        "distance": {"value": 0},
                        "duration": {"value": 0}
                    }
                ]
            }
        ]
    }
    distance_matrix = _build_distance_matrix(dummy_json, measure="duration")
    assert distance_matrix == [[0, 20], [20, 0]]
    distance_matrix = _build_distance_matrix(dummy_json, measure="distance")
    assert distance_matrix == [[0, 10], [10, 0]]
    with pytest.raises(AssertionError):
        _build_distance_matrix(dummy_json, measure="NOT A MEASURE")
