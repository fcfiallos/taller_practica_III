FROM python:3.10-slim

WORKDIR /app

COPY requirements.txt .
# ...existing code...
RUN pip install --no-cache-dir --default-timeout=100 -r requirements.txt
# ...existing code...
COPY . .

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
