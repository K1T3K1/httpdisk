from typing import Protocol, Any

class ObjectStorageProtocol(Protocol):
    """A protocol defining the interface for object storage operations."""

    async def get_object(self, path: str) -> Any:
        """Retrieve an object from the storage.

        Args:
            path (str): The path of the object.

        Returns:
            Any: The retrieved object.

        """

        pass

    async def create_object(self, path: str, data: bytes, overwrite: bool = False) -> bool:
        """Create an object in the storage.

        Args:
            path (str): The path of the object.
            data (bytes): The data to be stored in the object.
            overwrite (bool, optional): Whether to overwrite the object if it already exists. Defaults to False.

        Returns:
            bool: True if the object was created successfully, False otherwise.

        """

        pass

    async def delete_object(self, path: str) -> bool:
        """Delete an object from the storage.

        Args:
            path (str): The path of the object.

        Returns:
            bool: True if the object was deleted successfully, False otherwise.

        """

        pass

    async def list_objects(self, path: str) -> list[str]:
        """List objects in the storage under the given path.

        Args:
            path (str): The path to list objects under.

        Returns:
            list[str]: A list of object paths.

        """

        pass