from ..injector import Injector, DependencyProvider
from ..libraries.object_storage.azure_blob_storage import AzureBlobStorage
from ..repositories.disk.azure_disk import AzureDiskRepository
from ..repositories.disk.azure_disk_manager import AzureDiskManager
from ..repositories.file.azure_file_repository import AzureFileRepository
import os

def initialize():
    dependencies = []
    storage = AzureBlobStorage(
       os.getenv("BLOB_CONNECTION_STRING"), "test"
    )
    dependencies.append(DependencyProvider(instance=storage, name="object_storage"))

    dependencies.append(DependencyProvider(instance=AzureDiskRepository(storage), name="disk_repository"))
    dependencies.append(DependencyProvider(instance=AzureDiskManager(storage), name="disk_manager"))
    dependencies.append(DependencyProvider(instance=AzureFileRepository(storage), name="file_repository"))



    Injector.initialize(dependencies)
