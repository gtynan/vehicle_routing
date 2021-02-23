import pytest
import numpy as np

from src.tasks.distance_matrix import (
    get_distance_matrix,
    _build_distance_matrix,
    _send_request,
)


@pytest.mark.expensive
def test_get_distance_matrix():
    # 11 locations to ensure multiple requests must be sent
    locations = [
        "GAFFNEY CAR SALES, DELVIN, CO. WESTMEATH",
        "Marrowbone Lane, Saint Catherine's, Dublin, Ireland",
        "Cartow Vehicle Serivce, Finglas North, Dublin, Ireland",
        "VTN - West Auto Electric, Gortboy, Newcastle West, County Limerick, Ireland",
        "12 Ashling Heights, Corduff, Dublin 15, Ireland",
        "ALDI, Blackrock Avenue, Mahon, Cork, Ireland",
        "Renault Belgard Dublin, Belgard Road, Tallaght, Dublin 24, Ireland",
        "19 Charnwood Meadows, Clonsilla, Dublin, Ireland",
        "Coco nut, Long Mile Road, Walkinstown, Dublin, Ireland",
        "122 Castlecurragh Vale, Buzzardstown, Dublin 15, Ireland",
        "47 Castleknock Rise, Blanchardstown, Dublin 15, Ireland",
    ]
    full_matrix = np.array(get_distance_matrix(locations, [0]))
    sub_matrix = np.array(get_distance_matrix(locations[:3], [0]))

    # ensure full matrix has matching sub matrix
    np.testing.assert_array_equal(full_matrix[:3, :3], sub_matrix)

    assert len(full_matrix) == len(locations)
    assert all(full_matrix.diagonal() == 0)
    # ensure all off diagonal greate than 0
    # eye returns a k * k matrix with 1's on the diagonal
    assert all(full_matrix[~np.eye(len(full_matrix), dtype=bool)] > 0)


@pytest.mark.expensive
def test_get_distance_exclude_home():
    locations = [
        "GAFFNEY CAR SALES, DELVIN, CO. WESTMEATH",
        "Marrowbone Lane, Saint Catherine's, Dublin, Ireland",
        "Cartow Vehicle Serivce, Finglas North, Dublin, Ireland",
    ]
    driver_locs = [0, 2]
    matrix = np.array(get_distance_matrix(locations, driver_locs, return_home=False))
    assert np.all(matrix[:, driver_locs] == 0)


@pytest.mark.expensive
def test_send_request():
    str_locations = [
        "Cartow Vehicle Serivce, Finglas North, Dublin, Ireland",
        "Island Upper, County Wexford, Y25 A344, Ireland",
    ]
    coord_locations = [(53.39868, -6.29710), (52.67862, -6.39381)]

    location_response = _send_request(str_locations, str_locations, coordinates=False)
    location_response = _build_distance_matrix(location_response, measure="duration")

    coord_response = _send_request(coord_locations, coord_locations, coordinates=True)
    coord_response = _build_distance_matrix(coord_response, measure="duration")

    # coord and location not exactly equal so ensure ~equal
    precision_diff = (np.array(location_response) + 1) / (
        np.array(coord_response) + 1
    )  # add 1 to ensure no nans on diagonal
    np.testing.assert_almost_equal(precision_diff, 1)


def test_build_distance_matrix():
    # dummy json that matches whats expected from google
    dummy_json = {
        "rows": [
            {
                "elements": [
                    {"distance": {"value": 0}, "duration": {"value": 0}},
                    {"distance": {"value": 10}, "duration": {"value": 20}},
                ]
            },
            {
                "elements": [
                    {"distance": {"value": 10}, "duration": {"value": 20}},
                    {"distance": {"value": 0}, "duration": {"value": 0}},
                ]
            },
        ]
    }
    distance_matrix = _build_distance_matrix(dummy_json, measure="duration")
    assert distance_matrix == [[0, 20], [20, 0]]
    distance_matrix = _build_distance_matrix(dummy_json, measure="distance")
    assert distance_matrix == [[0, 10], [10, 0]]
    with pytest.raises(AssertionError):
        _build_distance_matrix(dummy_json, measure="NOT A MEASURE")
