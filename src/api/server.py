from fastapi import FastAPI
from src.api.routes.schedule_route import router as schedule_router
from src.api.routes.distance_route import router as distance_router

app = FastAPI(title="Pickup/Delivery POC")
app.include_router(distance_router)
app.include_router(schedule_router)
