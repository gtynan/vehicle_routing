from fastapi import FastAPI
from src.api.routes import router

app = FastAPI(title="Pickup Delivery MVP")
app.include_router(router)
