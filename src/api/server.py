from fastapi import FastAPI
from src.api.schedule import router as schedule_router
from src.api.distance import router as distance_router

app = FastAPI(title="Pickup/Delivery POC")
app.include_router(distance_router)
app.include_router(schedule_router)
