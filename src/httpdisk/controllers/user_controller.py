from fastapi.routing import APIRouter
from fastapi import Request, HTTPException
from fastapi_sso.sso.github import GithubSSO
from fastapi_sso.sso.base import OpenID
from fastapi.responses import RedirectResponse
import datetime

from jose import jwt 
import os
import logging

logger = logging.getLogger(__name__)

router = APIRouter()

SECRET_KEY = "<SMAD<MNSA<DNM"
CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")

API_PORT = os.getenv("API_PORT", 8000)

_sso = GithubSSO(
    client_id=CLIENT_ID,
    client_secret=CLIENT_SECRET,
    redirect_uri=f"http://localhost:{API_PORT}/auth/callback",
    allow_insecure_http=True,
)
@router.get("/user")
async def auth_init():
    logger.debug(f"CLIENT_ID: {CLIENT_ID}")
    logger.debug(f"CLIENT_SECRET: {CLIENT_SECRET}")
    with _sso:
        return await _sso.get_login_redirect()
    
@router.get("/auth/callback")
async def login_callback(request: Request):
    """Process login and redirect the user to the protected endpoint."""
    with _sso:
        openid = await _sso.verify_and_process(request)
        if not openid:
            raise HTTPException(status_code=401, detail="Authentication failed")
    # Create a JWT with the user's OpenID
    expiration = datetime.datetime.now(tz=datetime.timezone.utc) + datetime.timedelta(days=1)
    token = jwt.encode({"pld": openid.model_dump(), "exp": expiration, "sub": openid.id}, key=SECRET_KEY, algorithm="HS256")
    response = RedirectResponse(url="/disk")
    response.set_cookie(
        key="token", value=token, expires=expiration
    )  # This cookie will make sure /protected knows the user
    return response

@router.get("/auth/logout")
async def logout():
    """Forget the user's session."""
    response = RedirectResponse(url="/prot")
    response.delete_cookie(key="token")
    return response