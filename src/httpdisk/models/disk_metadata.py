from pydantic import BaseModel

class DiskMetadata(BaseModel):
    """
    Represents the metadata of a disk.

    Attributes:
        total_space (int): The total space of the disk in bytes.
    """
    total_space: int
    