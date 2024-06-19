import uvicorn
import os
from fastapi import FastAPI
from .controllers.user_controller import router as user_router
from .controllers.disk_controller import router as disk_router
from .controllers.file_controller import router as file_router
from .controllers.landing import router as landing_router
import logging
from fastapi.staticfiles import StaticFiles
from .dependencies.dev import initialize
from azure.monitor.opentelemetry import configure_azure_monitor

configure_azure_monitor()
logging.basicConfig(level=logging.INFO)

from contextlib import asynccontextmanager
from .injector import Injector

@asynccontextmanager
async def lifespan(app: FastAPI):
    await Injector._application_startup()
    yield
    await Injector._application_shutdown()

def main():
    initialize()
    app = FastAPI(lifespan=lifespan)
    app.mount("/templates", StaticFiles(directory="templates"), name="templates")
    app.include_router(user_router)
    app.include_router(disk_router)
    app.include_router(file_router)
    app.include_router(landing_router)
    return app

def start_server():
    port = int(os.getenv("API_PORT", 8000))
    uvicorn.run(main(), host="0.0.0.0", port=port, reload=False)
