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

# Install AI-related dependencies
RUN pip install --no-cache-dir \
    torch==2.0.1 \
    transformers==4.31.0 \
    scikit-learn==1.3.0 \
    pandas==2.0.3 \
    numpy==1.24.3

# Create necessary directories
RUN mkdir -p /app/ai/models

# Ensure alembic files are in the correct location
RUN mkdir -p /app/alembic/versions
COPY alembic.ini /app/

COPY alembic/env.py /app/alembic/
COPY alembic/script.py.mako /app/alembic/
COPY alembic/versions/001_initial_migration.py /app/alembic/versions/

# Copy application code
COPY app /app/app

# Add the application directory to Python path
ENV PYTHONPATH=/app
ENV PYTHONUNBUFFERED=1

# Expose port
EXPOSE 8000

# Copy startup script
COPY start.sh /app/start.sh
RUN chmod +x /app/start.sh

# Install netcat for database check
RUN apt-get update && apt-get install -y netcat-openbsd && rm -rf /var/lib/apt/lists/*

# Start the FastAPI application
CMD ["/app/start.sh"] 