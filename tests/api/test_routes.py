import pytest
from httpx import AsyncClient
from fastapi import FastAPI
from starlette.status import HTTP_404_NOT_FOUND, HTTP_200_OK
import json

from src.tasks.convert import route_list_to_model


class TestRoutes:

    @pytest.mark.asyncio
    async def test_routes_exist(self, app: FastAPI, client: AsyncClient) -> None:
        res = await client.post(app.url_path_for("routes:create_schedule"))
        assert res.status_code != HTTP_404_NOT_FOUND

    @pytest.mark.asyncio
    async def test_create_schedule(self, app: FastAPI, client: AsyncClient, mv_distance_matrix, pickup_deliver) -> None:
        data = json.dumps({
           "distance_matrix": mv_distance_matrix, 
           "pickup_delivery": pickup_deliver
        })
        
        res = await client.post(app.url_path_for("routes:create_schedule"), 
                                params={"n_vehicles": 4, "depot_node": 0}, 
                                data=data)

        assert res.status_code == HTTP_200_OK
        assert res.json() == route_list_to_model([[0, 16, 14, 13, 12, 0], 
                                                  [0, 7, 1, 6, 8, 0], 
                                                  [0, 4, 3, 15, 11, 0], 
                                                  [0, 5, 2, 10, 9, 0]])
