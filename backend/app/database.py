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


def get_x_accounts_collection():
    return get_db()["x_accounts"]


def get_x_oauth_states_collection():
    return get_db()["x_oauth_states"]


def init_indexes() -> None:
    get_users_collection().create_index("email", unique=True, sparse=True)
    get_users_collection().create_index("x_user_id", unique=True, sparse=True)
    get_predictions_collection().create_index([("user_id", 1), ("created_at", -1)])
    get_predictions_collection().create_index([("user_id", 1), ("source", 1), ("created_at", -1)])
    get_predictions_collection().create_index("x_tweet_id", sparse=True)
    get_x_accounts_collection().create_index("user_id", unique=True)
    get_x_accounts_collection().create_index("x_user_id", unique=True)
    get_x_oauth_states_collection().create_index("state", unique=True)
    get_x_oauth_states_collection().create_index("created_at", expireAfterSeconds=900)
