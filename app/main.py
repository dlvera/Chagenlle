from fastapi import FastAPI
from app.middleware.log_time import ResponseTimeLogger
from app.routers import posts, users, auth, tags
import logging

app = FastAPI(
    title="Dariel",
    description="Challenge",
    version="1.0.0",
    openapi_url="/openapi.json",
    docs_url="/docs",
    redoc_url="/redoc"
)

app.include_router(auth.router)
app.include_router(users.router)
app.include_router(posts.router)
app.include_router(tags.router)
app.add_middleware(ResponseTimeLogger)

@app.get("/")
def read_root():
    return {"message": "API funcionando"}


logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s - %(method)s - %(path)s - %(status)d - %(time_ms)s",
    level=logging.INFO
)