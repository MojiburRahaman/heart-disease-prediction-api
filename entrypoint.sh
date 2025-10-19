#!/bin/bash
set -e

# Check if model exists, if not train it
if [ ! -f "model/heart_model.joblib" ]; then
    echo "Model not found. Training model..."
    python model/model_run.py
    echo "Model training completed!"
fi

# Start the FastAPI application
echo "Starting API server..."
exec uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload --reload-dir /app/app --log-level info

