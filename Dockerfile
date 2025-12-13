FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

# Install curl for healthcheck
RUN apt-get update && apt-get install -y --no-install-recommends curl && \
    rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy server and supporting files
COPY server.py .
COPY sql_service.py .
# Copy chatbot UI files
COPY chatbot/ chatbot/

# Data directory will be mounted as volume
# COPY data/ data/

EXPOSE 8000

CMD ["fastmcp", "run", "server.py", "--transport", "http", "--host", "0.0.0.0", "--port", "8000"]
