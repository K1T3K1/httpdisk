from fastapi.responses import JSONResponse
from fastapi import UploadFile
from ..injector import Injector
from ..repositories.file.file_repository_protocol import FileRepositoryProtocol

@Injector.file_repository
async def upload_file(user_id: str, file: UploadFile, filename: str, file_repository: FileRepositoryProtocol) -> JSONResponse:
    """
    Uploads a file to the file repository.

    Args:
        user_id (str): The ID of the user uploading the file.
        file (UploadFile): The file to be uploaded.
        filename (str): The name of the file.
        file_repository (FileRepositoryProtocol): The file repository to store the file.

    Returns:
        JSONResponse: The response indicating the success or failure of the file upload.
    """
    file_data = await file.read()
    return await file_repository.create_file(user_id, filename, file_data)
    

@Injector.file_repository
async def delete_file(user_id: str, filename: str, file_repository: FileRepositoryProtocol):
    """
    Deletes a file for a given user.

    Args:
        user_id (str): The ID of the user.
        filename (str): The name of the file to be deleted.
        file_repository (FileRepositoryProtocol): The file repository used to delete the file.

    Returns:
        The result of the file deletion operation.
    """
    return await file_repository.delete_file(user_id, filename)

@Injector.file_repository
async def get_file(user_id: str, filename: str, file_repository: FileRepositoryProtocol):
    """
    Retrieves a file from the file repository.

    Args:
        user_id (str): The ID of the user.
        filename (str): The name of the file to retrieve.
        file_repository (FileRepositoryProtocol): The file repository to use.

    Returns:
        The contents of the file.

    """
    return await file_repository.read_file(user_id, filename)