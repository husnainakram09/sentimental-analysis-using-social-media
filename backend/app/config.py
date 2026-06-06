from functools import lru_cache
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "Sentiment Analysis API"
    app_env: str = "development"
    api_prefix: str = "/api/v1"
    allowed_origins: str = "http://localhost:5173,http://127.0.0.1:5173"
    mongodb_uri: str = "mongodb://localhost:27017"
    mongodb_db: str = "sentiment_app"
    sentiment_model_path: str = "app/models/sentiment_model.joblib"
    enable_db_logging: bool = True
    jwt_secret_key: str = "change_this_to_a_long_random_secret"
    jwt_algorithm: str = "HS256"
    jwt_access_token_expire_minutes: int = 1440

    x_client_id: str = ""
    x_client_secret: str = ""
    x_redirect_uri: str = ""
    x_scopes: str = "tweet.read users.read offline.access"
    x_auth_url: str = "https://x.com/i/oauth2/authorize"
    x_token_url: str = "https://api.x.com/2/oauth2/token"
    x_revoke_url: str = "https://api.x.com/2/oauth2/revoke"
    x_api_base_url: str = "https://api.x.com/2"

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    @property
    def cors_origins(self) -> list[str]:
        return [origin.strip() for origin in self.allowed_origins.split(",") if origin.strip()]

    @property
    def x_scope_list(self) -> list[str]:
        return [scope.strip() for scope in self.x_scopes.split() if scope.strip()]


@lru_cache
def get_settings() -> Settings:
    return Settings()
