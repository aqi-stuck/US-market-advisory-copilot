from typing import Optional

from fastapi import HTTPException, Security, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from app.core.config import settings

security = HTTPBearer(auto_error=False)


def get_api_key(
    credentials: Optional[HTTPAuthorizationCredentials] = Security(security),
) -> str:
    """
    If API_KEY is unset, allow requests in development mode.
    If API_KEY is set, require matching Bearer token.
    """
    if not settings.API_KEY:
        return credentials.credentials if credentials else "dev-mode"

    if not credentials or credentials.credentials != settings.API_KEY:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid API key",
            headers={"WWW-Authenticate": "Bearer"},
        )

    return credentials.credentials