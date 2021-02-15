import pytest

from src.tasks.distance_matrix import get_distance_matrix


@pytest.mark.asyncio
async def test_get_distance_matrix():
    test_locations = ['3610+Hacks+Cross+Rd+Memphis+TN', '1921+Elvis+Presley+Blvd+Memphis+TN',
                        '149+Union+Avenue+Memphis+TN','1034+Audubon+Drive+Memphis+TN']
    matrix = get_distance_matrix(test_locations)
    n = len(matrix)
    assert n == len(test_locations)

    for i in range(n):
        for j in range(n):
            if i == j:
                assert matrix[i][j] == 0 # diagonal should always be 0 
            else:
                assert matrix[i][j] > 0
