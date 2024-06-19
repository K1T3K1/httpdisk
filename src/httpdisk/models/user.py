from sqlmodel import SQLModel, Field
from typing import Literal, Optional

class User(SQLModel, table=True):
    """
    Represents a user in the system.

    Attributes:
        id (str): The unique identifier for the user.
        role (Optional[Literal["admin", "user"]]): The role of the user. Defaults to "user".
    """
    id: str = Field(primary_key=True)
    role: Optional[Literal["admin", "user"]] = Field(default="user")