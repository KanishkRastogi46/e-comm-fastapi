from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import Response, JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.gzip import GZipMiddleware
import uvicorn
from dotenv import load_dotenv
import os
from loguru import logger
from uuid import uuid4

from src.db import connect_db, disconnect_db

load_dotenv()

app = FastAPI(
    title="E-commerce FastAPI",
    description="A simple e-commerce application built with FastAPI and MongoDB.",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.add_middleware(
    GZipMiddleware,
    minimum_size=1024,
    compresslevel=9
)

from src.routers import products, orders
app.include_router(products.router)
app.include_router(orders.router)

from src.logging import config
logger.configure(**config)

@app.on_event("startup")
def startup_event():
    logger.info(f"Server running on {os.environ.get('HOST')}:{os.environ.get('SERVER_PORT')}")
    connect_db()
    
@app.on_event("shutdown")
def shutdown_event():
    disconnect_db()
    logger.info("Shutting down the server...")
    

@app.middleware("http")
async def log_requests(request: Request, call_next) -> Response:
    logger.info(f"Request: {request.method} {request.url}")
    correlation_id = request.headers.get('X-Request-ID', str(uuid4()))
    logger.info(f"Request ID: {correlation_id}")
    response = await call_next(request)
    response.headers['X-Request-ID'] = correlation_id
    logger.info(f"Response: {response.status_code}")
    return response


@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    logger.error(f"Unhandled exception: {exc}")
    return JSONResponse(
        status_code=500,
        content={"detail": "An unexpected error occurred. Please try again later.", "status_code": 500}
    )

@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    logger.error(f"HTTP exception: {exc.detail}")
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.detail, "status_code": exc.status_code}
    )
    
    
@app.get("/", tags=["Root"])
async def root():
    return {"message": "Welcome to the E-commerce API. Use /docs for API documentation."}

if __name__ == "__main__":
    uvicorn.run(app, host=os.environ.get('HOST'), port=int(os.environ.get("SERVER_PORT")))
    