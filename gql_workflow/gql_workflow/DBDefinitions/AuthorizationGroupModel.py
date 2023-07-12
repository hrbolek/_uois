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

class AuthorizationGroupModel(BaseModel):
    """Spravuje pristupove informace zalozene na skupinach"""

    __tablename__ = "awauthorizationgroups"

    id = UUIDColumn()
    authorization_id = Column(ForeignKey("awauthorizations.id"), index=True)
    #authorization = relationship("AuthorizationModel", back_populates="groupaccesses")
    group_id = UUIDFKey(nullable=True)#Column(ForeignKey("groups.id"), index=True)
    accesslevel = Column(Integer)

    created = Column(DateTime, server_default=sqlalchemy.sql.func.now(), comment="Fkey of user whi created this row")
    lastchange = Column(DateTime, server_default=sqlalchemy.sql.func.now())
    changedby = UUIDFKey(nullable=True)#Column(ForeignKey("users.id"), index=True, nullable=True)
    createdby = UUIDFKey(nullable=True)#Column(ForeignKey("users.id"), index=True, nullable=True)

