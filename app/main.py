from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from app.schemas import (
    HeartDiseaseInput, 
    PredictionResponse, 
    HealthResponse, 
    ModelInfo,
    ApiResponse
)
from app.predictor import HeartDiseasePredictor
from app.redis_client import RedisCache
import hashlib
import json
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(
    title="Heart Disease Prediction API",
    description="API for predicting heart disease using machine learning",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Initialize predictor
try:
    predictor = HeartDiseasePredictor()
    logger.info("Predictor initialized successfully")
except Exception as e:
    logger.error(f"Failed to initialize Predictor: {e}")
    predictor = None

# Initialize Redis cache
try:
    cache = RedisCache()
    logger.info("Redis Cache initialized")
except Exception as e:
    logger.warning(f"Redis Cache initialization failed: {e}")
    cache = None


# Exception handler for standardized error responses
@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "status": False,
            "message": exc.detail,
            "data": None
        }
    )


@app.exception_handler(Exception)
async def general_exception_handler(request: Request, exc: Exception):
    logger.error(f"Unhandled exception: {exc}")
    return JSONResponse(
        status_code=500,
        content={
            "status": False,
            "message": f"Internal server error: {str(exc)}",
            "data": None
        }
    )


@app.get("/", response_model=ApiResponse, tags=["Root"])
async def root():
    return ApiResponse(
        status=True,
        message="Heart Disease Prediction API",
        data={
            "version": "1.0.0",
            "docs": "/docs",
            "health": "/health"
        }
    )


@app.get("/health", response_model=ApiResponse, tags=["Health"])
async def health_check():
    if predictor is None or predictor.model is None:
        raise HTTPException(
            status_code=503,
            detail="Model not loaded. Service unavailable."
        )
    
    # Check Redis health
    redis_status = "connected" if cache and cache.health_check() else "disconnected"
    
    return ApiResponse(
        status=True,
        message=f"API is running, Model is loaded, Redis is {redis_status}",
        data={
            "health": "healthy",
            "model": "loaded",
            "redis": redis_status
        }
    )


@app.get("/info", response_model=ApiResponse, tags=["Model"])
async def get_model_info():
    """
    Get information about the model
    
    Returns model type, feature list, and other metadata
    """
    if predictor is None:
        raise HTTPException(
            status_code=503,
            detail="Model not loaded. Service unavailable."
        )
    
    try:
        info = predictor.get_model_info()
        return ApiResponse(
            status=True,
            message="Model information retrieved successfully",
            data=info
        )
    except Exception as e:
        logger.error(f"Error getting model info: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Error getting model information: {str(e)}"
        )


@app.post("/predict", response_model=ApiResponse, tags=["Prediction"])
async def predict_heart_disease(input_data: HeartDiseaseInput):
    """
    Predict heart disease presence
    
    Takes patient data as input and returns prediction with confidence.
    Results are cached in Redis for faster subsequent requests.
    """
    if predictor is None:
        raise HTTPException(
            status_code=503,
            detail="Model not loaded. Service unavailable."
        )
    
    try:
        # Convert Pydantic model to dict
        input_dict = input_data.model_dump()
        
        # Generate cache key from input data
        cache_key = f"prediction:{hashlib.md5(json.dumps(input_dict, sort_keys=True).encode()).hexdigest()}"
        
        # Try to get from cache
        cached = False
        if cache:
            cached_result = cache.get(cache_key)
            if cached_result:
                logger.info(f"Returning cached prediction: {cached_result}")
                result = cached_result
                cached = True
        
        # Make prediction if not cached
        if not cached:
            result = predictor.predict(input_dict)
            
            # Cache the result (TTL: 1 hour)
            if cache:
                cache.set(cache_key, result, ttl=3600)
            
            logger.info(f"Prediction made: {result}")
        
        return ApiResponse(
            status=True,
            message="Prediction completed successfully" + (" (from cache)" if cached else ""),
            data=result
        )
    
    except Exception as e:
        logger.error(f"Prediction error: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Prediction failed: {str(e)}"
        )


@app.delete("/cache/clear", response_model=ApiResponse, tags=["Cache"])
async def clear_cache():
    """
    Clear all cached predictions
    
    Useful for testing or when model is updated
    """
    if not cache:
        raise HTTPException(
            status_code=503,
            detail="Redis cache not available"
        )
    
    try:
        cache.clear()
        return ApiResponse(
            status=True,
            message="Cache cleared successfully",
            data=None
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to clear cache: {str(e)}"
        )


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

