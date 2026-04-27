from fastapi import FastAPI
from time import sleep, time
import logging

app = FastAPI()

logging.basicConfig(
    level=logging.INFO,
    format="Timestamp:%(asctime)s|Level:%(levelname)s|Message:%(message)s",
)
logger = logging.getLogger(__name__)


@app.get("/health")
def health():
    logger.info("Health check endpoint called")
    return {"status": "ok"}


@app.get("/slow")
def slow():
    start_time = time()
    sleep(2)
    duration_ms = int((time() - start_time) * 1000)
    logger.info("Slow endpoint called|ResponseTime:%sms", duration_ms)
    return {"status": "slow", "response_time_ms": duration_ms}


@app.get("/error")
def error():
    logger.error("Error endpoint called|Status:500")
    return {"status": "error", "code": 500}
