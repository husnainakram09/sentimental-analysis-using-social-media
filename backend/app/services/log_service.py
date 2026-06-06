from datetime import datetime, timezone
from ..config import get_settings
from ..database import get_predictions_collection


def build_log_doc(item: dict, user_id: str, source: str = "manual", metadata: dict | None = None) -> dict:
    doc = {
        "user_id": user_id,
        "text": item["text"],
        "label": item["label"],
        "confidence": item["confidence"],
        "probabilities": item["probabilities"],
        "source": source,
        "created_at": datetime.now(timezone.utc),
    }
    if metadata:
        doc.update(metadata)
    return doc


def log_prediction(item: dict, user_id: str, source: str = "manual", metadata: dict | None = None) -> None:
    settings = get_settings()
    if not settings.enable_db_logging:
        return
    get_predictions_collection().insert_one(build_log_doc(item, user_id, source=source, metadata=metadata))


def log_predictions(items: list[dict], user_id: str, source: str = "manual", metadata_builder=None) -> None:
    settings = get_settings()
    if not settings.enable_db_logging or not items:
        return
    docs = []
    for index, item in enumerate(items):
        metadata = metadata_builder(index, item) if metadata_builder else None
        docs.append(build_log_doc(item, user_id, source=source, metadata=metadata))
    get_predictions_collection().insert_many(docs)
