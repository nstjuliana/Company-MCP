# Company MCP Frontend
# Lightweight Python web server for the UI

FROM python:3.11-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application
COPY . .

# Expose port 80
EXPOSE 80

# Run the server
CMD ["python", "main.py"]



