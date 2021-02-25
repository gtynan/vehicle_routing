import pytest
from httpx import AsyncClient
from fastapi import FastAPI
from starlette.status import HTTP_404_NOT_FOUND, HTTP_200_OK
import json


class TestTimeRoute:
    @pytest.mark.asyncio
    async def test_routes_exist(self, app: FastAPI, client: AsyncClient) -> None:
        res = await client.post(app.url_path_for("time_matrix:create"))
        assert res.status_code != HTTP_404_NOT_FOUND

    @pytest.mark.expensive
    @pytest.mark.asyncio
    async def test_create_time_matrix(self, app: FastAPI, client: AsyncClient) -> None:
        data = {
            "locations": [
                "Marrowbone Lane, Saint Catherine's, Dublin, Ireland",
                "Cartow Vehicle Serivce, Finglas North, Dublin, Ireland",
            ],
            "driver_indicies": [0],
        }

        res = await client.post(
            app.url_path_for("time_matrix:create"),
            params={"return_home": False},
            data=json.dumps(data),
        )

        assert res.status_code == HTTP_200_OK

        assert res.json()["locations"] == data["locations"]
        assert res.json()["driver_indicies"] == data["driver_indicies"]
        assert isinstance(res.json()["matrix"], list)
        # from anywhere to depot should be 0 due to return home false
        assert res.json()["matrix"][1][0] == 0
