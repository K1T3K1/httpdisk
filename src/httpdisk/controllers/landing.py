from fastapi import Request
from fastapi.routing import APIRouter
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

router = APIRouter()

templates = Jinja2Templates(directory="templates")

@router.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    """
    Handler function for the root endpoint.
    
    Args:
        request (Request): The incoming request object.
    
    Returns:
        TemplateResponse: The rendered HTML template response.
    """
    return templates.TemplateResponse("index.html", {"request": request})