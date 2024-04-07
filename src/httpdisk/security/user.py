import os
from fastapi_sso.sso.base import OpenID
from fastapi import HTTPException, Security
from fastapi.security import APIKeyCookie
from jose import jwt

SECRET_KEY = "<SMAD<MNSA<DNM"

async def get_logged_user(cookie: str = Security(APIKeyCookie(name="token"))) -> OpenID:
    """Get user's JWT stored in cookie 'token', parse it and return the user's OpenID."""
    try:
        claims = jwt.decode(cookie, key=SECRET_KEY, algorithms=["HS256"])
        return OpenID(**claims["pld"])
    except Exception as error:
        raise HTTPException(status_code=401, detail="Invalid authentication credentials") from error