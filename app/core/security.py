import time, jwt
from pydantic import BaseModel
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from app.core.config import settings

bearer = HTTPBearer(auto_error=True)

class TokenPair(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
    expires_in: int

def _sign(payload: dict, ttl_min: int) -> str:
    now = int(time.time())
    exp = now + ttl_min * 60
    payload = {**payload, "iat": now, "exp": exp}
    return jwt.encode(payload, settings.JWT_PRIVATE_KEY, algorithm="HS256")

def issue_tokens(sub: str, role: str):
    access = _sign({"sub": sub, "role": role, "typ": "access"}, settings.JWT_TTL_MIN)
    refresh = _sign({"sub": sub, "role": role, "typ": "refresh"}, settings.JWT_REFRESH_TTL_MIN)
    return TokenPair(access_token=access, refresh_token=refresh, expires_in=settings.JWT_TTL_MIN*60)

def verify(token: str) -> dict:
    try:
        return jwt.decode(token, settings.JWT_PRIVATE_KEY, algorithms=["HS256"])
    except jwt.PyJWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="invalid_token")

def current_user_claims(creds: HTTPAuthorizationCredentials = Depends(bearer)) -> dict:
    claims = verify(creds.credentials)
    if claims.get("typ") != "access":
        raise HTTPException(status_code=401, detail="invalid_token_type")
    return claims

def require_role(*allowed):
    def dep(claims: dict = Depends(current_user_claims)):
        if claims.get("role") not in allowed:
            raise HTTPException(status_code=403, detail="forbidden")
        return claims
    return dep
