#!/bin/bash

# Set up environment
export PYTHONPATH=$PYTHONPATH:$(pwd)
export TEST_MODE=performance

# Run performance tests
echo "Running performance tests..."
pytest tests/performance/ -v --performance

# Run load tests
echo "Running load tests..."
locust -f tests/load/locustfile.py --config=tests/load/locust.conf.yaml

# Generate performance report
echo "Generating performance report..."
python scripts/generate_performance_report.py

# Run performance tests for critical endpoints
echo "Running performance tests..."

# Set test parameters
NUM_REQUESTS=1000
CONCURRENT_REQUESTS=50
BASE_URL="http://localhost:8000/api/v1"

# Run Python performance tests
python -m scripts.performance_tests \
    --endpoint="${BASE_URL}/health" \
    --num-requests=$NUM_REQUESTS \
    --concurrent-requests=$CONCURRENT_REQUESTS

python -m scripts.performance_tests \
    --endpoint="${BASE_URL}/threats/detect" \
    --num-requests=$NUM_REQUESTS \
    --concurrent-requests=$CONCURRENT_REQUESTS

# Check results against thresholds
if [ $? -eq 0 ]; then
    echo "Performance tests passed successfully"
    exit 0
else
    echo "Performance tests failed"
    exit 1
fi

echo "Performance testing completed!" 