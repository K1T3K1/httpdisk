from azure.storage.blob.aio import BlobServiceClient, StorageStreamDownloader
import asyncio
from typing import AsyncGenerator

class AzureBlobStorage:
    def __init__(self, connection_string: str, container_name: str):
        self.connection_string = connection_string
        self.container_name = container_name
        self.initialize = asyncio.create_task(self._initialize())
        

    async def _initialize(self):
        self.blob_service_client = BlobServiceClient.from_connection_string(self.connection_string)
        self.container_client = self.blob_service_client.get_container_client(self.container_name)


    async def context(self) -> AsyncGenerator[None, None]:
        await self.initialize


    async def get_object(self, path: str) -> StorageStreamDownloader[bytes]:
        blob_client = self.container_client.get_blob_client(path)
        return await blob_client.download_blob()
    
    async def create_object(self, path: str, data: bytes, overwrite: bool = False) -> bool:
        blob_client = self.container_client.get_blob_client(path)
        await blob_client.upload_blob(data, overwrite)
        return True
    
    async def delete_object(self, path: str) -> bool:
        blob_client = self.container_client.get_blob_client(path)
        await blob_client.delete_blob()
        return True