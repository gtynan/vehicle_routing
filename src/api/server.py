import logging
import time
import random
import string
from fastapi import FastAPI
from starlette.requests import Request
from src.api.routes.schedule_route import router as schedule_router
from src.api.routes.distance_route import router as distance_router

# setup loggers
logging.config.fileConfig("logging.conf", disable_existing_loggers=False)

# get root logger
logger = logging.getLogger(__name__)


app = FastAPI(title="Pickup/Delivery POC")
app.include_router(distance_router)
app.include_router(schedule_router)


@app.middleware("http")
async def log_requests(request: Request, call_next):
    idem = "".join(random.choices(string.ascii_uppercase + string.digits, k=6))
    logger.info(f"rid={idem} start request path={request.url.path}")
    start_time = time.time()

    response = await call_next(request)

    process_time = (time.time() - start_time) * 1000
    formatted_process_time = "{0:.2f}".format(process_time)
    logger.info(
        f"rid={idem} completed_in={formatted_process_time}ms status_code={response.status_code}"
    )
    return response
