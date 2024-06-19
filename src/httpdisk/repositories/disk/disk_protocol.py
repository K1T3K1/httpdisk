from typing import Protocol


class DiskProtocol(Protocol):
    """Interface for interacting with a disk storage system."""

    async def get_object(self, path: str) -> bytes | None:
        """Retrieve the object at the specified path.

        Args:
            path (str): The path of the object.

        Returns:
            bytes | None: The object data as bytes, or None if the object doesn't exist.
        """
        pass

    async def create_object(self, path: str, data: bytes, overwrite: bool = False) -> bool:
        """Create a new object at the specified path.

        Args:
            path (str): The path of the object.
            data (bytes): The data to be stored in the object.
            overwrite (bool, optional): Whether to overwrite an existing object with the same path. Defaults to False.

        Returns:
            bool: True if the object was created successfully, False otherwise.
        """
        pass

    async def delete_object(self, path: str) -> bool:
        """Delete the object at the specified path.

        Args:
            path (str): The path of the object.

        Returns:
            bool: True if the object was deleted successfully, False otherwise.
        """
        pass

    async def list_objects(self, path: str) -> list:
        """List all objects at the specified path.

        Args:
            path (str): The path to list objects from.

        Returns:
            list: A list of object names.
        """
        pass

    async def get_used_total_space(self, disk_name: str) -> tuple[int, int]:
        """Get the used and total space of a disk.

        Args:
            disk_name (str): The name of the disk.

        Returns:
            tuple[int, int]: A tuple containing the used space and total space in bytes.
        """
        pass
