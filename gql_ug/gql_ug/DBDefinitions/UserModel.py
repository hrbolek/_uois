import sqlalchemy
from sqlalchemy import (
    Column,
    String,
    DateTime,
    Boolean,
)
from sqlalchemy.orm import relationship

from .UUID import UUIDColumn, UUIDFKey
from .Base import BaseModel

class UserModel(BaseModel):
    """Spravuje data spojena s uzivatelem"""

    __tablename__ = "users"

    id = UUIDColumn()
    name = Column(String)
    surname = Column(String)
    email = Column(String)
    valid = Column(Boolean, default=True)
    startdate = Column(DateTime)
    enddate = Column(DateTime)

    memberships = relationship("MembershipModel", back_populates="user", foreign_keys="MembershipModel.user_id")
    roles = relationship("RoleModel", back_populates="user", foreign_keys="RoleModel.user_id")

    created = Column(DateTime, server_default=sqlalchemy.sql.func.now())
    lastchange = Column(DateTime, server_default=sqlalchemy.sql.func.now())
    createdby = UUIDFKey(nullable=True)#Column(ForeignKey("users.id"), index=True, nullable=True)
    changedby = UUIDFKey(nullable=True)#Column(ForeignKey("users.id"), index=True, nullable=True)


