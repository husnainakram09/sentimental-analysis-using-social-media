from datetime import datetime, timezone
from ..config import get_settings
from ..database import get_predictions_collection


def log_prediction(item: dict, user_id: str) -> None:
    settings = get_settings()
    if not settings.enable_db_logging:
        return
    doc = {
        "user_id": user_id,
        "text": item["text"],
        "label": item["label"],
        "confidence": item["confidence"],
        "probabilities": item["probabilities"],
        "created_at": datetime.now(timezone.utc),
    }
    get_predictions_collection().insert_one(doc)


def log_predictions(items: list[dict], user_id: str) -> None:
    settings = get_settings()
    if not settings.enable_db_logging or not items:
        return
    docs = [
        {
            "user_id": user_id,
            "text": item["text"],
            "label": item["label"],
            "confidence": item["confidence"],
            "probabilities": item["probabilities"],
            "created_at": datetime.now(timezone.utc),
        }
        for item in items
    ]
    get_predictions_collection().insert_many(docs)
