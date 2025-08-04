from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import logging

# Importa settings antes que cualquier otro módulo que lo use
from app.core.config import settings  # Cambia esta línea
from app.core.middleware.error_handler import sql_error_handler
from app.core.middleware.log_time import ResponseTimeLogger
from app.api.routers import comment, posts, users, auth, tags
from app.core.database import *


from sqlalchemy.exc import SQLAlchemyError

app = FastAPI(
    title="Dariel",
    description="Challenge",
    version="1.0.0",
    openapi_url="/openapi.json",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Configura CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Routers
app.include_router(auth.router)
app.include_router(users.router)
app.include_router(posts.router)
app.include_router(tags.router)
app.include_router(comment.router)

# Middleware
app.add_middleware(ResponseTimeLogger)

app.exception_handler(SQLAlchemyError)(sql_error_handler)

@app.get("/")
def read_root():
    return {"message": "API funcionando"}

logger = logging.getLogger()
logger.setLevel(logging.INFO)
handler = logging.StreamHandler()
formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
handler.setFormatter(formatter)
logger.addHandler(handler)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[logging.StreamHandler()]
)