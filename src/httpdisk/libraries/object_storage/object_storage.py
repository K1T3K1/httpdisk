from typing import Protocol, Any

class ObjectStorageProtocol(Protocol):
    async def get_object(self, path: str) -> Any:
        pass

    async def create_object(self, path: str, data: bytes, overwrite: bool = False) -> bool:
        pass

    async def delete_object(self, path: str) -> bool:
        pass