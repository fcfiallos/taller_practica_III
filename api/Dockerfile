FROM python:3.10-slim

WORKDIR /app

# 1. Instalar dependencias del sistema con reinstalación forzada
RUN apt-get update && apt-get install -y --no-install-recommends \
    libgl1 \
    libglib2.0-0 \
    libsm6 \
    libxext6 \
    libxrender1 \
    && rm -rf /var/lib/apt/lists/*

# 2. Instalar herramientas de compilación para posibles dependencias
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# 3. Instalar dependencias de Python
COPY requirements.txt .
RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# 4. Copiar la aplicación
COPY . .

# 5. Configurar Gunicorn para desarrollo
ENV GUNICORN_CMD_ARGS="--workers=1 --bind=0.0.0.0:5000 --timeout=120 --log-level=debug --reload"

EXPOSE 5000

CMD ["gunicorn", "app:app"]