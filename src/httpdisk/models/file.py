from pydantic import BaseModel
from fastapi import File, UploadFile

class UploadFileForm(BaseModel):
    """
    Represents a form for uploading a file.

    Attributes:
        file (UploadFile): The uploaded file.
        file_name (str): The name of the file.
    """
    file: UploadFile = File(...)
    file_name: str