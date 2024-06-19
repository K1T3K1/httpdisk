from ...libraries.object_storage.azure_blob_storage import AzureBlobStorage
from .consts import MANGLED
import logging
import json
import datetime

logger = logging.getLogger(__name__)


class AzureDiskManager:
    """
    Manages the creation, deletion, and existence checking of Azure disks.

    Args:
        storage (AzureBlobStorage): The Azure Blob Storage instance used for disk operations.
    """

    _metadata = f"{MANGLED}METADATA.json"

    def __init__(self, storage: AzureBlobStorage):
        self.storage = storage

    async def create_disk(self, user_id: str, user_email: str) -> bool:
        """
        Creates a disk for the specified user.

        Args:
            user_id (str): The ID of the user.
            user_email (str): The email address of the user.

        Returns:
            bool: True if the disk creation is successful, False otherwise.
        """
        try:
            await self.storage.create_object(f"{user_id}/{self._metadata}", json.dumps({"user_email": user_email}))
        except Exception as e:
            logger.critical({"time": datetime.datetime.now(), "message": "Failed to create a disk", "exception": e})
            return False
        return True

    async def delete_disk(self, user_id: str) -> bool:
        """
        Deletes the disk associated with the specified user.

        Args:
            user_id (str): The ID of the user.

        Returns:
            bool: True if the disk deletion is successful, False otherwise.
        """
        try:
            object = await self.storage.list_objects(user_id)
            for o in object:
                await self.storage.delete_object(o)
        except Exception as e:
            logger.critical({"time": datetime.datetime.now(), "message": "Failed to delete a disk", "exception": e})

            return False
        return True

    async def if_exists(self, user_id: str) -> bool:
        """
        Checks if a disk exists for the specified user.

        Args:
            user_id (str): The ID of the user.

        Returns:
            bool: True if a disk exists for the user, False otherwise.
        """
        try:
            object = await self.storage.list_objects(user_id)
            return bool(object)
        except Exception as e:
            logger.critical({"time": datetime.datetime.now(), "message": "Failed to check a disk", "exception": e})
            return False
