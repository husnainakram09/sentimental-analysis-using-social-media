from fastapi import APIRouter, Depends
from ..deps import get_current_user
from ..schemas import RegisterRequest, LoginRequest, AuthResponse, UserResponse
from ..services.auth_service import create_user, authenticate_user, create_access_token, serialize_user

router = APIRouter(prefix="/auth", tags=["Authentication"])


@router.post("/register", response_model=AuthResponse)
def register(payload: RegisterRequest):
    user = create_user(payload.name, payload.email, payload.password)
    token = create_access_token(str(user["_id"]))
    return {"access_token": token, "user": serialize_user(user)}


@router.post("/login", response_model=AuthResponse)
def login(payload: LoginRequest):
    user = authenticate_user(payload.email, payload.password)
    token = create_access_token(str(user["_id"]))
    return {"access_token": token, "user": serialize_user(user)}


@router.get("/me", response_model=UserResponse)
def me(current_user=Depends(get_current_user)):
    return serialize_user(current_user)
