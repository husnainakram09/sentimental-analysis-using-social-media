from __future__ import annotations
import base64
import hashlib
import secrets
from datetime import datetime, timezone
from urllib.parse import urlencode
import httpx
from fastapi import HTTPException, status
from ..config import get_settings
from ..database import get_x_accounts_collection, get_x_oauth_states_collection, get_predictions_collection
from .auth_service import get_or_create_x_user, create_access_token
from .model_service import model_service
from .log_service import log_predictions


def _b64url(data: bytes) -> str:
    return base64.urlsafe_b64encode(data).rstrip(b"=").decode("utf-8")


def generate_pkce_pair() -> tuple[str, str]:
    code_verifier = _b64url(secrets.token_bytes(32))
    code_challenge = _b64url(hashlib.sha256(code_verifier.encode("utf-8")).digest())
    return code_verifier, code_challenge


def create_login_url(frontend_url: str) -> str:
    settings = get_settings()
    if not settings.x_client_id or not settings.x_redirect_uri:
        raise HTTPException(status_code=500, detail="X OAuth is not configured on the server")

    state = secrets.token_urlsafe(24)
    code_verifier, code_challenge = generate_pkce_pair()
    get_x_oauth_states_collection().insert_one({
        "state": state,
        "code_verifier": code_verifier,
        "frontend_url": frontend_url.rstrip("/"),
        "created_at": datetime.now(timezone.utc),
    })

    params = {
        "response_type": "code",
        "client_id": settings.x_client_id,
        "redirect_uri": settings.x_redirect_uri,
        "scope": " ".join(settings.x_scope_list),
        "state": state,
        "code_challenge": code_challenge,
        "code_challenge_method": "S256",
    }
    return f"{settings.x_auth_url}?{urlencode(params)}"


def _token_headers() -> dict:
    settings = get_settings()
    headers = {"Content-Type": "application/x-www-form-urlencoded"}
    if settings.x_client_secret:
        basic = base64.b64encode(f"{settings.x_client_id}:{settings.x_client_secret}".encode()).decode()
        headers["Authorization"] = f"Basic {basic}"
    return headers


def _exchange_code(code: str, code_verifier: str) -> dict:
    settings = get_settings()
    data = {
        "code": code,
        "grant_type": "authorization_code",
        "client_id": settings.x_client_id,
        "redirect_uri": settings.x_redirect_uri,
        "code_verifier": code_verifier,
    }
    with httpx.Client(timeout=30) as client:
        response = client.post(settings.x_token_url, data=data, headers=_token_headers())
    if response.status_code >= 400:
        raise HTTPException(status_code=400, detail=f"X token exchange failed: {response.text}")
    return response.json()


def refresh_access_token(refresh_token: str) -> dict:
    settings = get_settings()
    data = {
        "refresh_token": refresh_token,
        "grant_type": "refresh_token",
        "client_id": settings.x_client_id,
    }
    with httpx.Client(timeout=30) as client:
        response = client.post(settings.x_token_url, data=data, headers=_token_headers())
    if response.status_code >= 400:
        raise HTTPException(status_code=400, detail="Unable to refresh X access token")
    return response.json()


def get_x_profile(access_token: str) -> dict:
    settings = get_settings()
    with httpx.Client(timeout=30) as client:
        response = client.get(
            f"{settings.x_api_base_url}/users/me",
            headers={"Authorization": f"Bearer {access_token}"},
            params={"user.fields": "profile_image_url,public_metrics,username,name"},
        )
    if response.status_code >= 400:
        raise HTTPException(status_code=400, detail=f"Unable to read X profile: {response.text}")
    return response.json().get("data", {})


def complete_oauth_login(code: str, state: str) -> dict:
    state_doc = get_x_oauth_states_collection().find_one({"state": state})
    if not state_doc:
        raise HTTPException(status_code=400, detail="Invalid or expired X login state")
    token_payload = _exchange_code(code, state_doc["code_verifier"])
    access_token = token_payload["access_token"]
    profile = get_x_profile(access_token)

    user = get_or_create_x_user(
        x_user_id=profile["id"],
        username=profile.get("username", "x-user"),
        name=profile.get("name") or profile.get("username", "X User"),
        profile_image_url=profile.get("profile_image_url"),
    )

    get_x_accounts_collection().update_one(
        {"user_id": str(user["_id"])},
        {"$set": {
            "user_id": str(user["_id"]),
            "x_user_id": profile["id"],
            "username": profile.get("username"),
            "name": profile.get("name"),
            "profile_image_url": profile.get("profile_image_url"),
            "access_token": access_token,
            "refresh_token": token_payload.get("refresh_token"),
            "scope": token_payload.get("scope"),
            "token_type": token_payload.get("token_type"),
            "updated_at": datetime.now(timezone.utc),
        }, "$setOnInsert": {"created_at": datetime.now(timezone.utc)}},
        upsert=True,
    )
    get_x_oauth_states_collection().delete_one({"state": state})

    return {
        "frontend_url": state_doc["frontend_url"],
        "token": create_access_token(str(user["_id"])),
    }


def get_connected_account(user_id: str):
    return get_x_accounts_collection().find_one({"user_id": user_id})


def _fetch_recent_tweets(access_token: str, x_user_id: str, max_results: int = 20) -> list[dict]:
    settings = get_settings()
    with httpx.Client(timeout=30) as client:
        response = client.get(
            f"{settings.x_api_base_url}/users/{x_user_id}/tweets",
            headers={"Authorization": f"Bearer {access_token}"},
            params={
                "max_results": max_results,
                "exclude": "retweets,replies",
                "tweet.fields": "created_at,lang,public_metrics",
            },
        )
    if response.status_code >= 400:
        raise HTTPException(status_code=400, detail=f"Unable to fetch tweets from X: {response.text}")
    return response.json().get("data", [])


def import_recent_tweets_for_user(user_id: str, max_results: int = 20) -> dict:
    if not model_service.is_ready():
        raise HTTPException(status_code=500, detail="Model is not loaded. Train the model first.")

    account = get_connected_account(user_id)
    if not account:
        raise HTTPException(status_code=400, detail="X account is not connected")

    access_token = account.get("access_token")
    if not access_token and account.get("refresh_token"):
        refreshed = refresh_access_token(account["refresh_token"])
        access_token = refreshed["access_token"]
        get_x_accounts_collection().update_one({"_id": account["_id"]}, {"$set": {"access_token": access_token, "refresh_token": refreshed.get("refresh_token", account.get("refresh_token")), "updated_at": datetime.now(timezone.utc)}})

    tweets = _fetch_recent_tweets(access_token, account["x_user_id"], max_results=max_results)
    existing_ids = set(
        doc["x_tweet_id"] for doc in get_predictions_collection().find({"user_id": user_id, "x_tweet_id": {"$exists": True}}, {"x_tweet_id": 1})
    )

    fresh_tweets = [tweet for tweet in tweets if tweet["id"] not in existing_ids and tweet.get("text", "").strip()]
    results = [model_service.predict(tweet["text"]) for tweet in fresh_tweets]

    def metadata_builder(index: int, item: dict):
        tweet = fresh_tweets[index]
        return {
            "x_tweet_id": tweet["id"],
            "x_permalink": f"https://x.com/{account.get('username')}/status/{tweet['id']}",
            "tweet_created_at": tweet.get("created_at"),
        }

    if results:
        log_predictions(results, user_id, source="x", metadata_builder=metadata_builder)

    return {
        "imported_count": len(results),
        "skipped_count": len(tweets) - len(results),
        "results": results,
    }


def build_x_profile_summary(user_id: str) -> dict:
    account = get_connected_account(user_id)
    if not account:
        return {"connected": False, "imported_tweet_count": 0}
    imported_count = get_predictions_collection().count_documents({"user_id": user_id, "source": "x"})
    return {
        "connected": True,
        "username": account.get("username"),
        "name": account.get("name"),
        "x_user_id": account.get("x_user_id"),
        "profile_image_url": account.get("profile_image_url"),
        "imported_tweet_count": imported_count,
    }
