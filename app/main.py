import os
import time

from fastapi import FastAPI, Response
from prometheus_client import Counter, generate_latest, CONTENT_TYPE_LATEST


app = FastAPI(
    title="DevOps Lab API",
    version=os.getenv("APP_VERSION", "development")
)


REQUEST_COUNT = Counter(
    "devops_lab_api_requests_total",
    "Total number of requests",
    ["endpoint"]
)


@app.get("/")
def root():
    REQUEST_COUNT.labels(endpoint="/").inc()

    return {
        "application": os.getenv("APP_NAME", "devops-lab-api"),
        "environment": os.getenv("APP_ENV", "development"),
        "version": os.getenv("APP_VERSION", "development"),
        "status": "running"
    }


@app.get("/health/live")
def liveness():
    REQUEST_COUNT.labels(endpoint="/health/live").inc()

    return {
        "status": "alive"
    }


@app.get("/health/ready")
def readiness():
    REQUEST_COUNT.labels(endpoint="/health/ready").inc()

    return {
        "status": "ready"
    }


@app.get("/version")
def version():
    REQUEST_COUNT.labels(endpoint="/version").inc()

    return {
        "application": os.getenv("APP_NAME", "devops-lab-api"),
        "version": os.getenv("APP_VERSION", "development")
    }


@app.get("/config")
def config():
    REQUEST_COUNT.labels(endpoint="/config").inc()

    return {
        "application": os.getenv("APP_NAME", "devops-lab-api"),
        "environment": os.getenv("APP_ENV", "development")
    }


@app.get("/load")
def load(seconds: int = 1):
    REQUEST_COUNT.labels(endpoint="/load").inc()

    seconds = max(1, min(seconds, 10))

    end_time = time.time() + seconds

    result = 0

    while time.time() < end_time:
        result += sum(i * i for i in range(10000))

    return {
        "status": "load-generated",
        "seconds": seconds
    }


@app.get("/metrics")
def metrics():
    return Response(
        content=generate_latest(),
        media_type=CONTENT_TYPE_LATEST
    )
