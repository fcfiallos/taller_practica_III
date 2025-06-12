FROM python:3.10-slim

WORKDIR /app

COPY main.py /app/

RUN pip install flask flask-cors hdfs tensorflow pillow numpy

CMD ["python", "main.py"]
