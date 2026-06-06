import hashlib
from datetime import datetime, timedelta, timezone
from bson import ObjectId
from jose import jwt, JWTError
from passlib.context import CryptContext
from fastapi import HTTPException, status
from ..config import get_settings
from ..database import get_users_collection

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(password: str):
    password = hashlib.sha256(password.encode()).hexdigest()
    return pwd_context.hash(password)


def verify_password(password: str, hashed: str):
    password = hashlib.sha256(password.encode()).hexdigest()
    return pwd_context.verify(password, hashed)


def create_access_token(user_id: str) -> str:
    settings = get_settings()
    expire = datetime.now(timezone.utc) + timedelta(minutes=settings.jwt_access_token_expire_minutes)
    payload = {"sub": user_id, "exp": expire}
    return jwt.encode(payload, settings.jwt_secret_key, algorithm=settings.jwt_algorithm)


def get_user_by_email(email: str):
    return get_users_collection().find_one({"email": email.lower().strip()})


def get_user_by_x_user_id(x_user_id: str):
    return get_users_collection().find_one({"x_user_id": x_user_id})


def create_user(name: str, email: str, password: str):
    collection = get_users_collection()
    if get_user_by_email(email):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email already registered")
    doc = {
        "name": name.strip(),
        "email": email.lower().strip(),
        "password_hash": hash_password(password),
        "auth_provider": "local",
        "x_connected": False,
        "created_at": datetime.now(timezone.utc),
    }
    result = collection.insert_one(doc)
    doc["_id"] = result.inserted_id
    return doc


def get_or_create_x_user(x_user_id: str, username: str, name: str, profile_image_url: str | None = None):
    collection = get_users_collection()
    user = get_user_by_x_user_id(x_user_id)
    if user:
        collection.update_one(
            {"_id": user["_id"]},
            {"$set": {
                "x_username": username,
                "name": name or user.get("name") or username,
                "x_profile_image_url": profile_image_url,
                "auth_provider": "x",
                "x_connected": True,
                "updated_at": datetime.now(timezone.utc),
            }}
        )
        user.update({
            "x_username": username,
            "name": name or user.get("name") or username,
            "x_profile_image_url": profile_image_url,
            "auth_provider": "x",
            "x_connected": True,
        })
        return user

    doc = {
        "name": name or username,
        "email": None,
        "password_hash": None,
        "auth_provider": "x",
        "x_user_id": x_user_id,
        "x_username": username,
        "x_profile_image_url": profile_image_url,
        "x_connected": True,
        "created_at": datetime.now(timezone.utc),
    }
    result = collection.insert_one(doc)
    doc["_id"] = result.inserted_id
    return doc


def authenticate_user(email: str, password: str):
    user = get_user_by_email(email)
    if not user or not user.get("password_hash") or not verify_password(password, user["password_hash"]):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid email or password")
    return user


def serialize_user(user) -> dict:
    return {
        "id": str(user["_id"]),
        "name": user["name"],
        "email": user.get("email"),
        "auth_provider": user.get("auth_provider", "local"),
        "x_username": user.get("x_username"),
        "x_connected": bool(user.get("x_connected")),
    }


def get_current_user_from_token(token: str):
    settings = get_settings()
    credentials_error = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid or expired token",
    )
    try:
        payload = jwt.decode(token, settings.jwt_secret_key, algorithms=[settings.jwt_algorithm])
        user_id = payload.get("sub")
        if not user_id:
            raise credentials_error
    except JWTError:
        raise credentials_error

    user = get_users_collection().find_one({"_id": ObjectId(user_id)})
    if not user:
        raise credentials_error
    return user
