from typing import Protocol

class DiskProtocol(Protocol):
    async def get_object(self, path: str) -> bytes | None:
        pass

    async def create_object(self, path: str, data: bytes, overwrite: bool = False) -> bool:
        pass

    async def delete_object(self, path: str) -> bool:
        pass

    async def list_objects(self, path: str) -> list:
        pass

    async def get_free_total_space(self, disk_name: str) -> tuple[int, int]:
        pass