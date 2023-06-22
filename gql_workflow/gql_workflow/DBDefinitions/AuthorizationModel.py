import sqlalchemy
from sqlalchemy import (
    Column,
    String,
    DateTime,
    Boolean,
    ForeignKey,
    Integer
)
from sqlalchemy.orm import relationship

from .UUID import UUIDColumn, UUIDFKey
from .Base import BaseModel


class AuthorizationModel(BaseModel):
    """Spravuje pristupove informace"""

    __tablename__ = "awauthorizations"

    id = UUIDColumn()