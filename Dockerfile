# Lesson 14 - Dockerfile for Meera's Bakery (FastAPI)
FROM python:3.11-slim

WORKDIR /code

# Install dependencies first (Docker caches this layer)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code and static files
COPY app ./app
COPY static ./static

EXPOSE 8000

# Module path is app.main:app (folder "app", file "main.py", object "app")
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
