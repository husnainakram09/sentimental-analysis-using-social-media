from fastapi import Depends
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from .services.auth_service import get_current_user_from_token

bearer_scheme = HTTPBearer(auto_error=True)


def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme)):
    return get_current_user_from_token(credentials.credentials)
