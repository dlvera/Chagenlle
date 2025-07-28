# Chagenlle - API con FastAPI

API moderna construida con FastAPI, SQLAlchemy 2.0 y Pydantic v2

## Requisitos

- Python 3.9+
- PostgreSQL 13+
- Poetry (opcional)

## Instalación

1. Clonar repositorio
2. Crear entorno virtual: `python -m venv venv`
3. Activar entorno:
   - Windows: `venv\Scripts\activate`
   - Unix: `source venv/bin/activate`
4. Instalar dependencias: `pip install -r requirements.txt`
5. Crear archivo .env basado en .env.example
6. Ejecutar: `uvicorn app.main:app --reload`

## Variables de Entorno

| Variable | Descripción | Ejemplo |
|----------|-------------|---------|
| DATABASE_URL | URL de conexión a PostgreSQL | postgresql+asyncpg://user:pass@localhost/dbname |
| SECRET_KEY | Clave para JWT | secreto-super-seguro |
| ALGORITHM | Algoritmo para JWT | HS256 |
| ACCESS_TOKEN_EXPIRE_MINUTES | Duración de tokens | 30 |

## Migraciones

Para crear/migrar la base de datos:
```bash
alembic revision --autogenerate -m "descripción"
alembic upgrade head