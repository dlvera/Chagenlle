import os
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    DATABASE_URL: str = os.getenv('DATABASE_URL') or \
        f"postgresql+asyncpg://{os.getenv('POSTGRES_USER')}:{os.getenv('POSTGRES_PASSWORD')}@{os.getenv('DB_HOST','db')}:5432/{os.getenv('POSTGRES_DB')}"
    
    SECRET_KEY: str = os.getenv('SECRET_KEY', 'default-insecure-key')
    ALGORITHM: str = os.getenv('ALGORITHM', 'HS256')
    DEBUG: bool = os.getenv('DEBUG', 'False').lower() == 'true'
    
    class Config:
        env_file = ".env"
        env_file_encoding = 'utf-8'

# Validación fuera de la clase
try:
    ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv('ACCESS_TOKEN_EXPIRE_MINUTES', '30'))
except ValueError:
    ACCESS_TOKEN_EXPIRE_MINUTES = 30

settings = Settings()
settings.ACCESS_TOKEN_EXPIRE_MINUTES = ACCESS_TOKEN_EXPIRE_MINUTES