from pymongo import MongoClient
from pymongo.database import Database
from .config import get_settings

_client: MongoClient | None = None


def get_client() -> MongoClient:
    global _client
    if _client is None:
        settings = get_settings()
        _client = MongoClient(settings.mongodb_uri)
    return _client


def get_db() -> Database:
    settings = get_settings()
    return get_client()[settings.mongodb_db]


def get_users_collection():
    return get_db()["users"]


def get_predictions_collection():
    return get_db()["predictions"]


def init_indexes() -> None:
    get_users_collection().create_index("email", unique=True)
    get_predictions_collection().create_index([("user_id", 1), ("created_at", -1)])
