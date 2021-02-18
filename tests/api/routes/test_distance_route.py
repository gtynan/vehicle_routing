import pytest
from httpx import AsyncClient
from fastapi import FastAPI
from starlette.status import HTTP_404_NOT_FOUND, HTTP_200_OK
import json



class TestDistanceRoute:

    @pytest.mark.asyncio
    async def test_routes_exist(self, app: FastAPI, client: AsyncClient) -> None:
        res = await client.post(app.url_path_for("distance_matrix:create"))
        assert res.status_code != HTTP_404_NOT_FOUND

    @pytest.mark.expensive
    @pytest.mark.asyncio
    async def test_create_schedule(self, app: FastAPI, client: AsyncClient) -> None:
        locations = ["Marrowbone Lane, Saint Catherine's, Dublin, Ireland", 
                     "Cartow Vehicle Serivce, Finglas North, Dublin, Ireland"]

        data = json.dumps(locations)
        res = await client.post(app.url_path_for("distance_matrix:create"), 
                                data=data)
        assert res.status_code == HTTP_200_OK
        assert res.json()["locations"] == locations
        assert isinstance(res.json()["matrix"], list)
