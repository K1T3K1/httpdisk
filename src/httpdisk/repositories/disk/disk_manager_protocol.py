from typing import Protocol

class DiskManagerProtocol(Protocol):
    """Interface for managing disks."""

    async def create_disk(self, user_id: str, user_email: str) -> bool:
        """Create a disk for the specified user.

        Args:
            user_id (str): The ID of the user.
            user_email (str): The email of the user.

        Returns:
            bool: True if the disk is created successfully, False otherwise.
        """
        pass

    async def delete_disk(self, user_id: str) -> bool:
        """Delete the disk for the specified user.

        Args:
            user_id (str): The ID of the user.

        Returns:
            bool: True if the disk is deleted successfully, False otherwise.
        """
        pass

    async def if_exists(self, user_id: str) -> bool:
        """Check if a disk exists for the specified user.

        Args:
            user_id (str): The ID of the user.

        Returns:
            bool: True if the disk exists, False otherwise.
        """
        pass
