# Etapa 1: Construcción
FROM python:3.11-slim-buster as builder

# Variables de entorno para Python
ENV PYTHONFAULTHANDLER=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=on \
    PIP_NO_CACHE_DIR=off \
    POETRY_VERSION=1.7.0

# Instalar dependencias del sistema y Poetry
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    curl \
    && rm -rf /var/lib/apt/lists/* \
    && pip install "poetry==$POETRY_VERSION"

# Establecer directorio de trabajo
WORKDIR /app

# Copiar archivos necesarios para instalar dependencias
COPY pyproject.toml poetry.lock* ./

# Instalar dependencias con pip
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
# Etapa 2: Imagen final
FROM python:3.11-slim-buster as runtime

# Instalar dependencias del sistema en tiempo de ejecución
RUN apt-get update && apt-get install -y \
    libpq5 \
    && rm -rf /var/lib/apt/lists/*

# Copiar dependencias instaladas desde la etapa de construcción
COPY --from=builder /usr/local/lib/python3.11/site-packages /usr/local/lib/python3.11/site-packages
COPY --from=builder /usr/local/bin /usr/local/bin

# Establecer directorio de trabajo
WORKDIR /app

# Copiar código de la aplicación
COPY . .

# Variables de entorno
ENV PYTHONPATH=/app \
    PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1

# Exponer puerto de la aplicación
EXPOSE 8000

# Comando para ejecutar la aplicación
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]

RUN adduser --disabled-password --gecos '' appuser
USER appuser

RUN chmod -R 755 /app && \
    find /app -type d -exec chmod 755 {} + && \
    find /app -type f -exec chmod 644 {} +