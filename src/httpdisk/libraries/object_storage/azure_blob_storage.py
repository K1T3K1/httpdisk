from azure.storage.blob.aio import BlobServiceClient, StorageStreamDownloader
from typing import AsyncGenerator


class AzureBlobStorage:
    def __init__(self, connection_string: str, container_name: str):
        """
        Initializes an instance of the AzureBlobStorage class.

        Args:
            connection_string (str): The connection string for the Azure Blob Storage account.
            container_name (str): The name of the container in the Azure Blob Storage account.
        """
        self.connection_string = connection_string
        self.container_name = container_name
        self.initialize = self._initialize()

    async def _initialize(self):
        """
        Initializes the Azure Blob Storage client by creating the BlobServiceClient and ContainerClient objects.

        This method should be called before performing any operations on the Azure Blob Storage.

        Raises:
            ValueError: If the connection string or container name is not provided.
        """
        self.blob_service_client = BlobServiceClient.from_connection_string(self.connection_string)
        self.container_client = self.blob_service_client.get_container_client(self.container_name)

    async def context(self) -> AsyncGenerator[None, None]:
        """
        A context manager that initializes the object storage and yields control.

        Usage:
        async with context() as _:
            # code to be executed within the context

        """
        await self.initialize
        yield

    async def get_object(self, path: str) -> StorageStreamDownloader[bytes]:
        """
        Retrieves an object from the Azure Blob Storage.

        Args:
            path (str): The path of the object to retrieve.

        Returns:
            StorageStreamDownloader[bytes]: The downloader object for the retrieved object.
        """
        blob_client = self.container_client.get_blob_client(path)
        return await blob_client.download_blob()

    async def create_object(self, path: str, data: bytes, overwrite: bool = False) -> bool:
        """
        Creates a new object in the Azure Blob Storage.

        Args:
            path (str): The path of the object in the storage.
            data (bytes): The data to be uploaded as the object content.
            overwrite (bool, optional): If set to True, overwrites the existing object with the same path.
                Defaults to False.

        Returns:
            bool: True if the object is created successfully, False otherwise.
        """
        blob_client = self.container_client.get_blob_client(path)
        await blob_client.upload_blob(data, overwrite=overwrite)
        return True

    async def delete_object(self, path: str) -> bool:
        """
        Deletes an object from the Azure Blob Storage.

        Args:
            path (str): The path of the object to be deleted.

        Returns:
            bool: True if the object is successfully deleted, False otherwise.
        """
        blob_client = self.container_client.get_blob_client(path)
        await blob_client.delete_blob()
        return True

    async def list_objects(self, prefix: str) -> list[str]:
        """
        Lists the objects in the Azure Blob Storage container that have the specified prefix.

        Args:
            prefix (str): The prefix to filter the object names.

        Returns:
            list[str]: A list of object names that match the specified prefix.
        """
        blobs = self.blob_service_client.get_container_client(self.container_name).list_blob_names(
            name_starts_with=prefix
        )
        return [blob async for blob in blobs]
