FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy server and supporting files
COPY server.py .
COPY _docs/map/ _docs/map/
COPY data/ data/

EXPOSE 8000

CMD ["fastmcp", "run", "server.py", "--transport", "http", "--host", "0.0.0.0", "--port", "8000"]
