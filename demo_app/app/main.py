from datetime import datetime
from pathlib import Path
from time import sleep, time
import logging

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

app = FastAPI()

LOG_DIR = Path(__file__).resolve().parents[1] / "logs"
LOG_DIR.mkdir(parents=True, exist_ok=True)
LOG_FILE = LOG_DIR / "app.log"

logger = logging.getLogger("demo_app")
logger.setLevel(logging.INFO)
logger.propagate = False

if not logger.handlers:
    formatter = logging.Formatter("%(message)s")

    file_handler = logging.FileHandler(LOG_FILE, encoding="utf-8")
    file_handler.setFormatter(formatter)

    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(formatter)

    logger.addHandler(file_handler)
    logger.addHandler(stream_handler)


def write_log(request: Request, status_code: int, response_time_ms: int) -> None:
    forwarded_for = request.headers.get("x-forwarded-for")
    if forwarded_for:
        client_ip = forwarded_for.split(",")[0].strip()
    else:
        client_ip = request.client.host if request.client else "unknown"

    log_line = "Timestamp:{}|IP:{}|Path:{}|Status:{}|ResponseTime:{}ms".format(
        datetime.now().isoformat(),
        client_ip,
        request.url.path,
        status_code,
        response_time_ms,
    )

    if status_code >= 500:
        logger.error(log_line)
    else:
        logger.info(log_line)


@app.get("/health")
def health(request: Request):
    start_time = time()

    response = {"status": "ok"}

    duration_ms = int((time() - start_time) * 1000)
    write_log(request, 200, duration_ms)

    return response


@app.get("/slow")
def slow(request: Request):
    start_time = time()

    sleep(2)
    response = {"status": "slow"}

    duration_ms = int((time() - start_time) * 1000)
    write_log(request, 200, duration_ms)

    return response


@app.get("/error")
def error(request: Request):
    start_time = time()

    duration_ms = int((time() - start_time) * 1000)
    write_log(request, 500, duration_ms)

    return JSONResponse(
        status_code=500,
        content={"status": "error", "code": 500},
    )
