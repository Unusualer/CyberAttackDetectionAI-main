# Use Python 3.11 slim as base
FROM python:3.11.7-slim-bullseye

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    git \
    libpq-dev \
    libffi-dev \
    && rm -rf /var/lib/apt/lists/*

# Configure pip for better reliability
RUN pip config set global.timeout 1000 && \
    pip config set global.retries 10 && \
    pip config set global.index-url https://pypi.org/simple && \
    pip install --no-cache-dir --upgrade pip setuptools wheel

# Install Python dependencies in stages to better handle failures
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the backend code
COPY . .

# Add the application directory to Python path
ENV PYTHONPATH=/app
ENV PYTHONUNBUFFERED=1

# Expose port
EXPOSE 8000

# Create startup script
RUN echo '#!/bin/sh\n\
# Wait for database\n\
echo "Waiting for database..."\n\
while ! nc -z db 5432; do\n\
  sleep 1\n\
done\n\
echo "Database is ready!"\n\
\n\
# Initialize database with single worker\n\
echo "Initializing database..."\n\
uvicorn app.main:app --host 0.0.0.0 --port 8000 --workers 1\n\
' > /app/start.sh && chmod +x /app/start.sh

# Install netcat for database check
RUN apt-get update && apt-get install -y netcat-openbsd && rm -rf /var/lib/apt/lists/*

# Start the FastAPI application
CMD ["/app/start.sh"] 