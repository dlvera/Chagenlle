from logging.config import fileConfig
from alembic import context
from sqlalchemy.ext.asyncio import create_async_engine
import asyncio
from app.models import Base  # Asegúrate que esta importación sea correcta

# Configuración de Alembic
config = context.config

# Configurar logging
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# Metadatos para autogenerate
target_metadata = Base.metadata

def run_migrations_offline():
    """Ejecuta migraciones en modo offline (sin conexión a BD)."""
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )
    with context.begin_transaction():
        context.run_migrations()

def run_migrations_online():
    """Ejecuta migraciones en modo asíncrono."""
    connectable = create_async_engine(config.get_main_option("sqlalchemy.url"))

    async def run_async_migrations():
        async with connectable.connect() as connection:
            await connection.run_sync(do_run_migrations)

    asyncio.run(run_async_migrations())

def do_run_migrations(connection):
    context.configure(
        connection=connection,
        target_metadata=target_metadata,
        compare_type=True,
    )
    with context.begin_transaction():
        context.run_migrations()

# Punto de entrada principal
if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()