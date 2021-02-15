from fastapi import FastAPI
from src.api.schedule import router

app = FastAPI(title="Pickup Delivery MVP")
app.include_router(router)
