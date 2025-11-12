from __future__ import annotations

import time
import uuid
from typing import Any, Dict, Tuple

import jwt

from app.core.config import settings

def _now() -> int:
    return int(time.time())

def issue_access_refresh(
        *,
        sub: str,
        role: str,
        access_ttl_min: int | None = None,
        refresh_ttl_min: int | None = None,
) -> Tuple[str, str]:
    secret = settings.JWT_PRIVATE_KEY
    alg = "HS256"
    iss = "threat-intel-api"

    iat = _now()
    at_exp = iat + 60 * (access_ttl_min or settings.JWT_TTL_MIN)
    rt_exp = iat + 60 * (refresh_ttl_min or settings.JWT_REFRESH_TTL_MIN)

    access_payload: Dict[str, Any] = {
        "iss": iss,
        "iat": iat,
        "exp": at_exp,
        "sub": sub,
        "role":  role,
        "typ": "access",
        "ver": 1,
    }

    refresh_payload: Dict[str, Any] = {
        "iss": iss,
        "iat": iat,
        "exp": rt_exp,
        "sub": sub,
        "role":  role,
        "typ": "refresh",
        "ver": 1,
        "jti": str(uuid.uuid4())
    }

    access_token = jwt.encode(access_payload, secret, algorithm=alg)
    refresh_token = jwt.encode(refresh_payload, secret, algorithm=alg)
    return access_token, refresh_token

def decode_jwt(token: str) -> Dict[str, Any]:
    return jwt.decode(
        token,
        settings.JWT_PRIVATE_KEY,
        algorithms=["HS256"],
        options={"require": ["exp", "sub", "typ"]},
    )