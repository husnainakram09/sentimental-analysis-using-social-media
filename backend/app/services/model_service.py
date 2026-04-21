from __future__ import annotations
import joblib
from pathlib import Path
from .prediction_service import build_prediction
from ..config import get_settings


class ModelService:
    def __init__(self):
        self.model = None

    def load_model(self):
        settings = get_settings()
        path = Path(settings.sentiment_model_path)
        if not path.exists():
            raise FileNotFoundError(f"Model file not found at {path}")
        self.model = joblib.load(path)

    def is_ready(self) -> bool:
        return self.model is not None

    def predict(self, text: str) -> dict:
        if self.model is None:
            raise RuntimeError("Model is not loaded")
        return build_prediction(self.model, text)


model_service = ModelService()
