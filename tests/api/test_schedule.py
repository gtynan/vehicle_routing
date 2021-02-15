import pytest
from httpx import AsyncClient
from fastapi import FastAPI
from starlette.status import HTTP_404_NOT_FOUND, HTTP_200_OK
import json

from src.models.schedule import Schedule
from src.tasks.routing import get_routes

class TestRoutes:

    @pytest.mark.asyncio
    async def test_routes_exist(self, app: FastAPI, client: AsyncClient) -> None:
        res = await client.post(app.url_path_for("schedule:create"))
        assert res.status_code != HTTP_404_NOT_FOUND

    @pytest.mark.asyncio
    async def test_create_schedule(self, app: FastAPI, client: AsyncClient, mv_distance_matrix, pickup_deliver) -> None:
        data = json.dumps({
           "distance_matrix": mv_distance_matrix, 
           "pickup_delivery": pickup_deliver
        })
        
        res = await client.post(app.url_path_for("schedule:create"), 
                                params={"n_vehicles": 4, "depot_node": 0}, 
                                data=data)

        assert res.status_code == HTTP_200_OK
        assert res.json() == [Schedule.from_raw(driver_id=i, route=row, distance_matrix=mv_distance_matrix).dict() \
                                for i, row in enumerate(get_routes(mv_distance_matrix, 4, 0, pickup_deliver))]
