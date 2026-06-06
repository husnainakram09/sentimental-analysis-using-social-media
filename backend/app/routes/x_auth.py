from urllib.parse import quote
from fastapi import APIRouter, Depends, Query
from fastapi.responses import RedirectResponse
from ..deps import get_current_user
from ..schemas import XAuthStartResponse, XProfileResponse, XImportResponse
from ..services.x_service import create_login_url, complete_oauth_login, build_x_profile_summary, import_recent_tweets_for_user

router = APIRouter(prefix="/x", tags=["X Integration"])


@router.get("/auth/login", response_model=XAuthStartResponse)
def x_auth_login(frontend_url: str = Query(..., min_length=1)):
    return {"authorization_url": create_login_url(frontend_url)}


@router.get("/auth/callback")
def x_auth_callback(code: str, state: str):
    payload = complete_oauth_login(code, state)
    redirect_url = f"{payload['frontend_url']}/?x_token={quote(payload['token'])}"
    return RedirectResponse(url=redirect_url, status_code=302)


@router.get("/me", response_model=XProfileResponse)
def x_me(current_user=Depends(get_current_user)):
    return build_x_profile_summary(str(current_user["_id"]))


@router.post("/import-self", response_model=XImportResponse)
def import_self_tweets(max_results: int = 10, current_user=Depends(get_current_user)):
    return import_recent_tweets_for_user(str(current_user["_id"]), max_results=max_results)
