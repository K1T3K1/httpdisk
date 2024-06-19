from ...libraries.object_storage.azure_blob_storage import AzureBlobStorage
import logging
from azure.core.exceptions import ResourceExistsError
from .consts import MANGLED
from ...models.disk_metadata import DiskMetadata
import datetime

logger = logging.getLogger(__name__)


class AzureDiskRepository:
    _metadata = f"{MANGLED}METADATA.json"

    def __init__(self, storage: AzureBlobStorage):
        self.storage = storage

    async def get_object(self, path: str) -> bytes | None:
        """
        Retrieves the object at the specified path from the storage.

        Args:
            path (str): The path of the object to retrieve.

        Returns:
            bytes | None: The content of the object as bytes, or None if the object does not exist or an error occurs.
        """
        try:
            data = await self.storage.get_object(path)
        except Exception as e:
            return None
        return await data.readall()

    async def create_object(self, path: str, data: bytes, overwrite: bool = False) -> bool:
        """
        Creates an object at the specified path in the Azure disk storage.

        Args:
            path (str): The path where the object should be created.
            data (bytes): The data to be stored in the object.
            overwrite (bool, optional): Whether to overwrite the object if it already exists. Defaults to False.

        Returns:
            bool: True if the object was created successfully, False otherwise.
        """
        try:
            await self.storage.create_object(path, data, overwrite)
        except ResourceExistsError as ree:
            return False
        except Exception as e:
            logger.critical({"time": datetime.datetime.now(), "message": "Failed to create an object", "exception": e})

            return False
        return True

    async def delete_object(self, path: str) -> bool:
        """
        Deletes an object at the specified path.

        Args:
            path (str): The path of the object to be deleted.

        Returns:
            bool: True if the object is successfully deleted, False otherwise.
        """
        try:
            return await self.storage.delete_object(path)
        except Exception as e:
            logger.critical({"time": datetime.datetime.now(), "message": "Failed to delete an object", "exception": e})
        return False

    async def list_objects(self, path: str) -> list[str]:
        """
        Lists objects in the Azure disk storage container.

        Args:
            path (str): The path to list objects from.

        Returns:
            list[str]: A list of object names.

        Raises:
            Exception: If there is an error listing objects.
        """
        blobs = []
        try:
            blob_list = self.storage.container_client.list_blobs(name_starts_with=path)
            async for blob in blob_list:
                logger.critical(f"Blob: {blob.name}")
                if not MANGLED in blob.name:
                    blobs.append(blob.name.split("/")[-1])
        except Exception as e:
            logger.critical({"time": datetime.datetime.now(), "message": "Failed to list objects", "exception": e})
        return blobs

    async def get_used_total_space(self, disk_name: str) -> tuple[int, int]:
        """
        Retrieves the used and total space of a disk.

        Args:
            disk_name (str): The name of the disk.

        Returns:
            tuple[int, int]: A tuple containing the used space and total space of the disk.
        """
        try:
            blobs = self.storage.container_client.list_blobs(name_starts_with=disk_name)
        except Exception as e:
            logger.critical({"time": datetime.datetime.now(), "message": "Failed to get used up space", "exception": e})
            return (0, 0)

        used_space = 0
        async for b in blobs:
            used_space += b.size

        total_space = await self._get_total_space(disk_name)

        return (used_space, total_space)

    async def _get_total_space(self, disk_name: str) -> int:
        """
        Retrieves the total space of a disk.

        Args:
            disk_name (str): The name of the disk.

        Returns:
            int: The total space of the disk.

        Raises:
            None

        """
        try:
            metadata = await self.get_object(f"{disk_name}/{self._metadata}")
        except Exception as e:
            logger.critical({"time": datetime.datetime.now(), "message": "Failed to get used up space", "exception": e})
            return 0

        try:
            metadata_model = DiskMetadata.model_validate_json(metadata)
        except Exception as e:
            logger.critical({"time": datetime.datetime.now(), "message": "Failed to validate metadata", "exception": e})
            return 0

        return metadata_model.total_space
