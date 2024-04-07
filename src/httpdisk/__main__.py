import uvicorn
import os
from fastapi import FastAPI
from .controllers.user_controller import router as user_router
from .controllers.disk_controller import router as disk_router
from .controllers.landing import router as landing_router
import logging
from fastapi.staticfiles import StaticFiles

logging.basicConfig(level=logging.DEBUG)
def main():
    app = FastAPI()
    app.mount("/templates", StaticFiles(directory="templates"), name="templates")
    app.include_router(user_router)
    app.include_router(disk_router)
    app.include_router(landing_router)
    return app

def start_server():
    port = os.getenv("API_PORT", 8000)
    uvicorn.run(main(), host="0.0.0.0", port=port, reload=False)
