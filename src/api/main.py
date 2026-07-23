from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
import time

from src.api.routers import (
    health,
    companies,
    screener,
    sectors,
    peers,
    valuation,
    portfolio,
    documents,
)

API_VERSION = "1.0.0"

app = FastAPI(
    title="Nifty100 Financial Intelligence API",
    version=API_VERSION,
    description="REST API for the Nifty100 Financial Intelligence Platform"
)

# ---------------------------------------------------------
# CORS Middleware
# ---------------------------------------------------------

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ---------------------------------------------------------
# Request Logging Middleware
# ---------------------------------------------------------

@app.middleware("http")
async def log_requests(request: Request, call_next):

    start_time = time.time()

    response = await call_next(request)

    process_time = (time.time() - start_time) * 1000

    print(
        f"{request.method} "
        f"{request.url.path} "
        f"- {response.status_code} "
        f"- {process_time:.2f} ms"
    )

    return response


# ---------------------------------------------------------
# Root Endpoint
# ---------------------------------------------------------

@app.get("/")
def root():
    return {
        "message": "Nifty100 Financial Intelligence API is running."
    }


# ---------------------------------------------------------
# API Routers
# ---------------------------------------------------------

app.include_router(
    health.router,
    prefix="/api/v1",
    tags=["Health"]
)

app.include_router(
    companies.router,
    prefix="/api/v1",
    tags=["Companies"]
)

app.include_router(
    screener.router,
    prefix="/api/v1",
    tags=["Screener"]
)

app.include_router(
    sectors.router,
    prefix="/api/v1",
    tags=["Sectors"]
)

app.include_router(
    peers.router,
    prefix="/api/v1",
    tags=["Peers"]
)

app.include_router(
    valuation.router,
    prefix="/api/v1",
    tags=["Valuation"]
)

app.include_router(
    portfolio.router,
    prefix="/api/v1",
    tags=["Portfolio"]
)

app.include_router(
    documents.router,
    prefix="/api/v1",
    tags=["Documents"]
)