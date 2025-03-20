from pydantic_settings import BaseSettings  

class Settings(BaseSettings):
    # Configuración de la base de datos (desde variables de entorno o valor por defecto)
    DATABASE_URL: str = "postgresql+asyncpg://postgres:postgres@localhost:5432/fastapi"
    
    # Nueva variable para seguridad (cargada desde .env)
    SECRET_KEY: str = "clave_temporal_cambiar_en_produccion"  # 🚨 Reemplazar en producción!
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    class SettingsConfigDict:
        env_file = ".env"  # Carga variables desde archivo .env

settings = Settings()

