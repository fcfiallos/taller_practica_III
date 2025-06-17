# Usamos la MISMA imagen que los workers de Spark como base.
# Esto garantiza la compatibilidad de versiones.
FROM bitnami/spark:latest

# Cambiamos al usuario root para poder instalar paquetes
USER root

# Instalar pip y luego las dependencias de Python desde requirements.txt
RUN apt-get update -qq && \
    apt-get install -y -qq python3-pip && \
    apt-get clean
COPY requirements.txt .
RUN pip3 install --no-cache-dir -r requirements.txt

# Establecer el directorio de trabajo
WORKDIR /app

# Cambiar de nuevo al usuario por defecto de la imagen de Bitnami (opcional, pero buena práctica)
USER 1001

# Comando para iniciar Jupyter Lab
CMD ["python3", "-m", "jupyter", "lab", "--ip=0.0.0.0", "--port=8888", "--allow-root", "--no-browser", "--NotebookApp.token=''"]