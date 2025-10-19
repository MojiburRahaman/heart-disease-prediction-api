import logging
from pathlib import Path
from typing import Any, Dict, Literal

import joblib
import numpy as np

# Configure logging
logger = logging.getLogger(__name__)

# Constants
FEATURE_NAMES = [
    "age", "sex", "cp", "trestbps", "chol", "fbs",
    "restecg", "thalach", "exang", "oldpeak", "slope", "ca", "thal"
]
MODEL_PATH = "model/heart_model.joblib"
MODEL_VERSION = "1.0.0"
MODEL_DESCRIPTION = "Binary classifier for heart disease prediction"

# Risk level thresholds
HIGH_RISK_THRESHOLD = 0.7
MODERATE_RISK_THRESHOLD = 0.3


class HeartDiseasePredictor:
    def __init__(self, model_path: str = MODEL_PATH) -> None:
        self.model_path = Path(model_path)
        self.model = self._load_model()
        self.feature_names = FEATURE_NAMES

    def _load_model(self) -> Any:
        if not self.model_path.exists():
            raise FileNotFoundError(f"Model file not found at {self.model_path}")

        model = joblib.load(self.model_path)
        return model
    def predict(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        features_array = self._prepare_features(input_data)
        prediction = self.model.predict(features_array)[0]
        confidence = self._calculate_confidence(features_array, prediction)
        risk_level = self._determine_risk_level(prediction, confidence)

        return {
            "heart_disease": bool(prediction),
            "confidence": confidence,
            "risk_level": risk_level
        }

    def _prepare_features(self, input_data: Dict[str, Any]) -> np.ndarray:
        features = [input_data[feature] for feature in self.feature_names]
        return np.array(features).reshape(1, -1)

    def _calculate_confidence(self, features_array: np.ndarray, prediction: int) -> float:
        if hasattr(self.model, 'predict_proba'):
            proba = self.model.predict_proba(features_array)[0]
            return float(proba[int(prediction)])
        return 0.75

    def _determine_risk_level(
        self, 
        prediction: int, 
        confidence: float
    ) -> Literal["low", "moderate", "high"]:
        if prediction == 0:
            return "low"
        
        # For positive predictions, classify by confidence
        if confidence >= HIGH_RISK_THRESHOLD:
            return "high"
        elif confidence >= MODERATE_RISK_THRESHOLD:
            return "moderate"
        else:
            return "low"

    def get_model_info(self) -> Dict[str, Any]:
        return {
            "model_type": type(self.model).__name__,
            "features": self.feature_names,
            "description": MODEL_DESCRIPTION,
            "version": MODEL_VERSION
        }

