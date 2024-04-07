from ...libraries.object_storage.azure_blob_storage import AzureBlobStorage
import logging
from azure.core.exceptions import ResourceExistsError
from .consts import MANGLED
from ...models.disk_metadata import DiskMetadata

logger = logging.getLogger(__name__)

class AzureDiskRepository:
    _metadata = f"{MANGLED}METADATA.json"

    def __init__(self, storage: AzureBlobStorage):
        self.storage = storage

    async def get_object(self, path: str) -> bytes | None:
        try:
            data = await self.storage.get_object(path)
        except Exception as e:
            return None
        return data.readall()
    
    async def create_object(self, path: str, data: bytes, overwrite: bool = False) -> bool:
        try:
            await self.storage.create_object(path, data, overwrite)
        except ResourceExistsError as ree:
            logger.error(f"Resource already exists: {ree}")
            False
        except Exception as e:
            logger.error(f"Error creating object: {e}")
            return False
        return True
    
    async def delete_object(self, path: str) -> bool:
        try:
            return await self.storage.delete_object(path)
        except Exception as e:
            logger.error(f"Error deleting object: {e}")
        return False
    
    async def list_objects(self, path: str) -> list:
        blobs = []
        try:
            blob_list = self.storage.container_client.list_blobs(name_starts_with=path)
            async for blob in blob_list:
                if not blob.name.startswith(MANGLED):
                    blobs.append(blob.name)
        except Exception as e:
            logger.error(f"Error listing objects: {e}")
        return []
    
    async def get_used_total_space(self, disk_name: str) -> tuple[int, int]:
        try:
            blobs = self.storage.container_client.list_blobs(name_starts_with=disk_name)
        except Exception as e:
            logger.error(f"Error getting free total space: {e}")
            return (0, 0)
        
        used_space = 0
        async for b in blobs:
            used_space += b.size

        total_space = await self._get_total_space(disk_name)

        return (used_space, total_space)

    
    async def _get_total_space(self, disk_name: str) -> int:
        try:
            metadata = await self.get_object(f"{disk_name}/{self._metadata}")
        except Exception as e:
            logger.error(f"Error getting total space: {e}")
            return 0
        
        try:
            metadata_model = DiskMetadata.model_validate_json(metadata)
        except Exception as e:
            logger.error(f"Error validating metadata: {e}")
            return 0
        
        return metadata_model.total_space