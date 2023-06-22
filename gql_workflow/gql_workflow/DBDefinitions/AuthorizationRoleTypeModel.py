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

class AuthorizationRoleTypeModel(BaseModel):
    """Spravuje pristupove informace zalozene na rolich ve skupinach"""

    __tablename__ = "awauthorizationroletypes"

    id = UUIDColumn()
    authorization_id = Column(ForeignKey("awauthorizations.id"), index=True)
    #authorization = relationship("AuthorizationModel", back_populates="roletypeacesses")
    group_id = UUIDFKey(nullable=True)#ForeignKey("groups.id"), index=True)
    roletype_id = UUIDFKey(nullable=True)#Column(ForeignKey("roletypes.id"), index=True)
    accesslevel = Column(Integer)

    created = Column(DateTime, server_default=sqlalchemy.sql.func.now())
    lastchange = Column(DateTime, server_default=sqlalchemy.sql.func.now())
    changedby = UUIDFKey(nullable=True)#Column(ForeignKey("users.id"), index=True, nullable=True)
    createdby = UUIDFKey(nullable=True)#Column(ForeignKey("users.id"), index=True, nullable=True)

