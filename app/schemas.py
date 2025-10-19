from enum import IntEnum
from typing import Any, List, Literal

from pydantic import BaseModel, Field


class Sex(IntEnum):
    FEMALE = 0
    MALE = 1


class ChestPainType(IntEnum):
    TYPICAL_ANGINA = 0
    ATYPICAL_ANGINA = 1
    NON_ANGINAL_PAIN = 2
    ASYMPTOMATIC = 3


class FastingBloodSugar(IntEnum):
    LESS_THAN_120 = 0
    GREATER_THAN_120 = 1


class RestingECG(IntEnum):
    NORMAL = 0
    ST_T_WAVE_ABNORMALITY = 1
    LEFT_VENTRICULAR_HYPERTROPHY = 2


class ExerciseInducedAngina(IntEnum):
    NO = 0
    YES = 1


class STSlope(IntEnum):
    UPSLOPING = 0
    FLAT = 1
    DOWNSLOPING = 2


class Thalassemia(IntEnum):"
    NORMAL = 0
    FIXED_DEFECT = 1
    REVERSIBLE_DEFECT = 2
    UNKNOWN = 3


# Type aliases
RiskLevel = Literal["low", "moderate", "high"]


class ApiResponse(BaseModel):
    status: bool = Field(..., description="Indicates whether the request was successful")
    message: str = Field(..., description="Human-readable message describing the response")
    data: Any = Field(default=None, description="Response payload data (nullable)")

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "status": True,
                    "message": "Request processed successfully",
                    "data": {"result": "example"}
                }
            ]
        }
    }


class HeartDiseaseInput(BaseModel):
    # Demographics
    age: int = Field(
        ...,
        ge=0,
        le=120,
        description="Patient age in years",
        examples=[63]
    )
    sex: int = Field(
        ...,
        ge=0,
        le=1,
        description="Biological sex (0 = female, 1 = male)",
        examples=[1]
    )
    
    # Symptoms
    cp: int = Field(
        ...,
        ge=0,
        le=3,
        description="Chest pain type (0 = typical angina, 1 = atypical angina, 2 = non-anginal pain, 3 = asymptomatic)",
        examples=[3]
    )
    exang: int = Field(
        ...,
        ge=0,
        le=1,
        description="Exercise induced angina (0 = no, 1 = yes)",
        examples=[0]
    )
    
    # Vital Signs & Lab Results
    trestbps: int = Field(
        ...,
        ge=0,
        le=300,
        description="Resting blood pressure in mm Hg on admission to hospital",
        examples=[145]
    )
    chol: int = Field(
        ...,
        ge=0,
        le=600,
        description="Serum cholesterol in mg/dl",
        examples=[233]
    )
    fbs: int = Field(
        ...,
        ge=0,
        le=1,
        description="Fasting blood sugar > 120 mg/dl (0 = false, 1 = true)",
        examples=[1]
    )
    thalach: int = Field(
        ...,
        ge=0,
        le=250,
        description="Maximum heart rate achieved during exercise test",
        examples=[150]
    )
    
    # ECG & Stress Test Results
    restecg: int = Field(
        ...,
        ge=0,
        le=2,
        description="Resting electrocardiographic results (0 = normal, 1 = ST-T wave abnormality, 2 = left ventricular hypertrophy)",
        examples=[0]
    )
    oldpeak: float = Field(
        ...,
        ge=0.0,
        le=10.0,
        description="ST depression induced by exercise relative to rest",
        examples=[2.3]
    )
    slope: int = Field(
        ...,
        ge=0,
        le=2,
        description="Slope of the peak exercise ST segment (0 = upsloping, 1 = flat, 2 = downsloping)",
        examples=[0]
    )
    
    # Imaging & Blood Tests
    ca: int = Field(
        ...,
        ge=0,
        le=4,
        description="Number of major vessels (0-4) colored by fluoroscopy",
        examples=[0]
    )
    thal: int = Field(
        ...,
        ge=0,
        le=3,
        description="Thalassemia (0 = normal, 1 = fixed defect, 2 = reversible defect, 3 = unknown)",
        examples=[1]
    )

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "age": 63,
                    "sex": 1,
                    "cp": 3,
                    "trestbps": 145,
                    "chol": 233,
                    "fbs": 1,
                    "restecg": 0,
                    "thalach": 150,
                    "exang": 0,
                    "oldpeak": 2.3,
                    "slope": 0,
                    "ca": 0,
                    "thal": 1
                },
                {
                    "age": 52,
                    "sex": 0,
                    "cp": 2,
                    "trestbps": 125,
                    "chol": 212,
                    "fbs": 0,
                    "restecg": 1,
                    "thalach": 168,
                    "exang": 0,
                    "oldpeak": 1.0,
                    "slope": 1,
                    "ca": 2,
                    "thal": 2
                }
            ]
        }
    }


class PredictionResponse(BaseModel):
    heart_disease: bool = Field(
        ...,
        description="Indicates presence of heart disease (true) or absence (false)"
    )
    confidence: float = Field(
        ...,
        ge=0.0,
        le=1.0,
        description="Model confidence score ranging from 0 (low confidence) to 1 (high confidence)"
    )
    risk_level: RiskLevel = Field(
        ...,
        description="Categorical risk assessment: 'low' (<0.3), 'moderate' (0.3-0.7), 'high' (>0.7)"
    )

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "heart_disease": True,
                    "confidence": 0.85,
                    "risk_level": "high"
                },
                {
                    "heart_disease": False,
                    "confidence": 0.92,
                    "risk_level": "low"
                }
            ]
        }
    }


class HealthResponse(BaseModel):
    """Health check response indicating service availability"""
    status: str = Field(..., description="Service status", examples=["healthy"])
    message: str = Field(..., description="Detailed status message", examples=["Service is running"])

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "status": "healthy",
                    "message": "All systems operational"
                }
            ]
        }
    }


class ModelInfo(BaseModel):
    """Model information and metadata response"""
    model_type: str = Field(..., description="Type of ML model used", examples=["Random Forest Classifier"])
    features: List[str] = Field(..., description="List of feature names used by the model")
    description: str = Field(..., description="Model description and purpose")
    version: str = Field(..., description="Model version identifier", examples=["1.0.0"])

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "model_type": "Random Forest Classifier",
                    "features": ["age", "sex", "cp", "trestbps", "chol"],
                    "description": "Heart disease prediction model trained on UCI dataset",
                    "version": "1.0.0"
                }
            ]
        }
    }

