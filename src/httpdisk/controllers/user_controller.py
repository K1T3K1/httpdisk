from fastapi.routing import APIRouter
from fastapi import Request, HTTPException
from fastapi_sso.sso.github import GithubSSO
from fastapi_sso.sso.base import OpenID
from fastapi.responses import RedirectResponse
import datetime
import os
from jose import jwt 
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
    redirect_uri=f"{os.getenv('REDIRECT_URL')}/auth/callback",
    allow_insecure_http=True,
)
@router.get("/user")
async def auth_init():
    """
    Initialize the authentication process.

    This function retrieves the CLIENT_ID and CLIENT_SECRET from the logger,
    and then calls the `_sso.get_login_redirect()` function to get the login redirect URL.

    Returns:
        The login redirect URL.

    """
    logger.critical(f"REDIRECT_URL: {os.getenv('REDIRECT_URL')}")
    with _sso:
        return await _sso.get_login_redirect()
    
@router.get("/auth/callback")
async def login_callback(request: Request):
    """
    Process login and redirect the user to the protected endpoint.

    Args:
        request (Request): The incoming request object.

    Returns:
        RedirectResponse: The redirect response object.

    Raises:
        HTTPException: If authentication fails.
    """
    with _sso:
        openid = await _sso.verify_and_process(request)
        if not openid:
            raise HTTPException(status_code=401, detail="Authentication failed")

    expiration = datetime.datetime.now(tz=datetime.timezone.utc) + datetime.timedelta(days=1)
    token = jwt.encode({"pld": openid.model_dump(), "exp": expiration, "sub": openid.id}, key=SECRET_KEY, algorithm="HS256")
    response = RedirectResponse(url="/disk")
    response.set_cookie(
        key="token", value=token, expires=expiration
    )
    
    return response

@router.get("/auth/logout")
async def logout():
    """
    Forget the user's session.

    This function is responsible for logging out the user by deleting the session token cookie.

    Returns:
        RedirectResponse: A redirect response to the "/prot" URL.
    """
    response = RedirectResponse(url="/prot")
    response.delete_cookie(key="token")
    return response