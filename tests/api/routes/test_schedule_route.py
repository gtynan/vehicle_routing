import pytest
from httpx import AsyncClient
from fastapi import FastAPI
from starlette.status import (
    HTTP_404_NOT_FOUND,
    HTTP_200_OK,
    HTTP_422_UNPROCESSABLE_ENTITY,
)
import json
import numpy as np


class TestScheduleRoute:
    @pytest.mark.asyncio
    async def test_routes_exist(self, app: FastAPI, client: AsyncClient) -> None:
        res = await client.post(app.url_path_for("schedule:create"))
        assert res.status_code != HTTP_404_NOT_FOUND

    @pytest.mark.asyncio
    async def test_create_schedule(
        self, app: FastAPI, client: AsyncClient, mv_distance_matrix, pickup_deliver
    ) -> None:

        data = json.dumps(
            {
                "time_matrix": mv_distance_matrix,
                "delivery_pairs": pickup_deliver,
                "depot_nodes": [0] * 4,
            }
        )
        res = await client.post(
            app.url_path_for("schedule:create"),
            data=data,
        )
        assert res.status_code == HTTP_200_OK

        # create an impossible matrix to solve
        data = json.dumps(
            {
                "time_matrix": (np.array(mv_distance_matrix) * 10000).tolist(),
                "delivery_pairs": pickup_deliver,
                "depot_nodes": [0] * 4,
            }
        )
        res = await client.post(
            app.url_path_for("schedule:create"),
            data=data,
        )
        assert res.status_code == HTTP_422_UNPROCESSABLE_ENTITY
