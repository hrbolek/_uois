import sqlalchemy
from sqlalchemy import (
    Column,
    String,
    ForeignKey,
    DateTime,
    Boolean,
)
from sqlalchemy.orm import relationship

from .UUID import UUIDColumn, UUIDFKey
from .Base import BaseModel


class RoleModel(BaseModel):
    """Spojuje uzivatele a skupinu, ve ktere uzivatel "hraje" roli"""

    __tablename__ = "roles"

    id = UUIDColumn()
    user_id = Column(ForeignKey("users.id"), index=True)
    group_id = Column(ForeignKey("groups.id"), index=True)
    roletype_id = Column(ForeignKey("roletypes.id"), index=True)

    startdate = Column(DateTime)
    enddate = Column(DateTime)
    valid = Column(Boolean)

    created = Column(DateTime, server_default=sqlalchemy.sql.func.now())
    lastchange = Column(DateTime, server_default=sqlalchemy.sql.func.now())
    createdby = UUIDFKey(nullable=True)#Column(ForeignKey("users.id"), index=True, nullable=True)
    changedby = UUIDFKey(nullable=True)#Column(ForeignKey("users.id"), index=True, nullable=True)


    roletype = relationship("RoleTypeModel", back_populates="roles")
    user = relationship("UserModel", back_populates="roles", foreign_keys=[user_id])
    group = relationship("GroupModel", back_populates="roles")
