from ..injector import Injector
from fastapi import Depends
from ..repositories.disk.disk_manager_protocol import DiskManagerProtocol
from ..repositories.disk.disk_protocol import DiskProtocol
from fastapi.responses import JSONResponse
import logging

logger = logging.getLogger(__name__)

@Injector.disk_manager
async def create_disk(user_id: str, user_email: str, disk_manager: DiskManagerProtocol = Depends()) -> JSONResponse:
    """
    Create a disk for a user.

    Args:
        user_id (str): The ID of the user.
        user_email (str): The email of the user.
        disk_manager (DiskManagerProtocol, optional): The disk manager instance. Defaults to Depends().

    Returns:
        JSONResponse: The response indicating whether the disk was created or not.
    """
    result = await disk_manager.create_disk(user_id, user_email)


    if result:
        return JSONResponse(content={"message": "Disk created"}, status_code=201)
    return JSONResponse(content={"message": "Disk not created"}, status_code=400)

@Injector.disk_manager
async def check_disk(user_id: str, disk_manager: DiskManagerProtocol = Depends) -> JSONResponse:
    """
    Check if a disk exists for the given user ID.

    Args:
        user_id (str): The ID of the user.
        disk_manager (DiskManagerProtocol, optional): The disk manager instance. Defaults to Depends.

    Returns:
        JSONResponse: The result of the disk existence check.
    """
    result = await disk_manager.if_exists(user_id)

    return result

@Injector.disk_repository
async def list_disk_elements(user_id: str, disk_repository: DiskProtocol = Depends()) -> JSONResponse:
    """
    Retrieve a list of disk elements for a given user.

    Args:
        user_id (str): The ID of the user.
        disk_repository (DiskProtocol, optional): The disk repository to use. Defaults to Depends().

    Returns:
        JSONResponse: The response containing the list of disk elements.
    """
    result = await disk_repository.list_objects(user_id)
    return result