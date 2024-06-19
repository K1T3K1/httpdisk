from fastapi.routing import APIRouter
from fastapi import Depends, Request
from ..security.user import get_logged_user
from fastapi_sso.sso.base import OpenID
from ..helpers.disk import create_disk as create_disk_helper
from ..helpers.disk import check_disk as check_disk_helper
from ..helpers.disk import list_disk_elements
from fastapi.templating import Jinja2Templates
import logging
import datetime
logger = logging.getLogger(__name__)

router = APIRouter()

templates = Jinja2Templates(directory="templates")


@router.post("/disk")
async def create_disk(
    user: OpenID = Depends(get_logged_user),
):
    """
    Create a disk for the logged-in user.

    Parameters:
    - user: The logged-in user's OpenID.

    Returns:
    - The response from the create_disk_helper function.
    """
    logger.info({
            "time": datetime.datetime.now(),
            "message": "Creating disk for user",
        })
    response = await create_disk_helper(user.id, user.email)
    return response

@router.get("/upload")
async def upload_file_form(request: Request):
    """
    Renders the upload file form.

    Parameters:
    - request (Request): The incoming request object.

    Returns:
    - TemplateResponse: The response containing the rendered upload file form.
    """
    return templates.TemplateResponse("upload_file_form.html", context={"request": request})

@router.get("/disk")
async def read_disk(request: Request, user: OpenID = Depends(get_logged_user)):
    """
    Read the disk contents for a specific user.

    Args:
        request (Request): The incoming request object.
        user (OpenID): The logged-in user.

    Returns:
        TemplateResponse: The template response containing the disk contents or the create disk form.
    """
    exists = await check_disk_helper(user.id)
    if exists:
        elements = await list_disk_elements(user.id)
        return templates.TemplateResponse("disk.html", context={"request": request, "elements": elements})
    return templates.TemplateResponse("create_disk_form.html", context={"request": request})

