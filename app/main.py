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
    
    return ApiResponse(
        status=True,
        message="API is running, Model is loaded",
        data={
            "health": "healthy",
            "model": "loaded"
        }
    )


@app.get("/info", response_model=ApiResponse, tags=["Model"])
async def get_model_info():
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
    if predictor is None:
        raise HTTPException(
            status_code=503,
            detail="Model not loaded. Service unavailable."
        )
    
    try:
        # Convert Pydantic model to dict
        input_dict = input_data.model_dump()
        
        # Make prediction
        result = predictor.predict(input_dict)
        logger.info(f"Prediction made: {result}")
        
        return ApiResponse(
            status=True,
            message="Prediction completed successfully",
            data=result
        )
    
    except Exception as e:
        logger.error(f"Prediction error: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Prediction failed: {str(e)}"
        )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

