from fastapi.routing import APIRouter
from fastapi import Depends
from ..security.user import get_logged_user
from fastapi_sso.sso.base import OpenID

router = APIRouter()

@router.post("/disk")
async def create_disk(user: OpenID = Depends(get_logged_user)):
    return {"message": "Disk created"}

@router.get("/disk")
async def read_disk(user: OpenID = Depends(get_logged_user)):
    return {"message": "Disk read"}