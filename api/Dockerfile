FROM python:3.9

# Instalar Java 8 y curl
RUN apt-get update && apt-get install -y \
    openjdk-8-jdk \
    curl \
    && apt-get clean

# Variables de entorno para Java
ENV JAVA_HOME=/usr/lib/jvm/java-8-openjdk-amd64
ENV PATH="$JAVA_HOME/bin:$PATH"

# Crear directorios necesarios
WORKDIR /app
RUN mkdir -p /app/temp /app/models /app/spark-jobs

# Copiar archivos
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiar código fuente
COPY main.py .
COPY spark-jobs/preprocess_image.py ./spark-jobs/

# Comando por defecto
CMD ["python", "main.py"]
