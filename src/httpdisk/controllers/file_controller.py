from fastapi.routing import APIRouter
from fastapi import UploadFile, Depends, Request, File, Form
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse, Response
from ..security.user import get_logged_user
from fastapi_sso.sso.base import OpenID
from ..helpers.file import upload_file, delete_file, get_file
import starlette.status as status

from typing import Optional
import logging

logger = logging.getLogger(__name__)
router = APIRouter()

templates = Jinja2Templates(directory="templates")

@router.post("/upload")
async def upload_file_endpoint(request: Request, files: list[UploadFile] = File(...), filenames: list[Optional[str]] = Form(...), user: OpenID = Depends(get_logged_user)):
    """
    Uploads files to the server.

    Args:
        request (Request): The incoming request object.
        files (list[UploadFile]): The list of files to be uploaded.
        filenames (list[Optional[str]]): The list of optional filenames for the files.
        user (OpenID): The logged-in user.

    Returns:
        TemplateResponse: The response containing the rendered template.
    """
    for idx, file in enumerate(files):
        if not filenames[idx]:
            filename = file.filename
        else:
            filename = filenames[idx]

        result = await upload_file(user.id, file, filename)

    return templates.TemplateResponse("upload_file_form.html", context={"request": request})

@router.post("/file/")
async def delete_file_endpoint(request: Request, filename: str = Form(...), user: OpenID = Depends(get_logged_user)):
    """
    Delete a file from the disk.

    Args:
        request (Request): The incoming request.
        filename (str): The name of the file to be deleted.
        user (OpenID): The logged-in user.

    Returns:
        RedirectResponse: A redirect response to the "/disk" endpoint.
    """
    result = await delete_file(user.id, filename)
    
    return RedirectResponse("/disk", status_code=status.HTTP_302_FOUND)

@router.get("/file/{filename}", response_class=Response)
async def get_file_endpoint(request: Request, filename: str, user: OpenID = Depends(get_logged_user)):
    """
    Retrieve a file from the server.

    Args:
        request (Request): The incoming request object.
        filename (str): The name of the file to retrieve.
        user (OpenID): The logged-in user.

    Returns:
        Response: The file content as a response object with the appropriate headers.
    """
    result = await get_file(user.id, filename)    

    return Response(result, headers={"Content-Disposition": "attachment"})