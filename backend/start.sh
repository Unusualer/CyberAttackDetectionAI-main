#!/bin/sh

echo "Waiting for database..."
while ! nc -z db 5432; do
  sleep 1
done
echo "Database is ready!"

# Initialize database with single worker
echo "Initializing database..."

# Run database migrations
cd /app
export PYTHONPATH=/app
# Try to merge heads if multiple exist
alembic merge heads -m "merge_multiple_heads" || true
# Then upgrade to head
alembic upgrade heads || exit 1  # Use 'heads' instead of 'head'

# Wait a moment for the database to be ready after migrations
sleep 2

# Initialize database with initial data
cd /app && python -c "
from app.db.session import SessionLocal
from app.db.init_db import init_db
db = SessionLocal()
init_db(db)
"

# Initialize ML data
cd /app && python -m app.services.ml.init_data

uvicorn app.main:app --host 0.0.0.0 --port 8000 --workers 1 