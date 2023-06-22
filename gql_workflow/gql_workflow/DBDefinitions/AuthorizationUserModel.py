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

class AuthorizationUserModel(BaseModel):
    """Spravuje pristupove informace zalozene na uzivatelich"""

    __tablename__ = "awauthorizationusers"

    id = UUIDColumn()
    authorization_id = Column(ForeignKey("awauthorizations.id"), index=True)
    #authorization = relationship("AuthorizationModel", back_populates="useraccesses")
    user_id = UUIDFKey(nullable=True)#Column(ForeignKey("users.id"), index=True)
    accesslevel = Column(Integer)

    created = Column(DateTime, server_default=sqlalchemy.sql.func.now())
    lastchange = Column(DateTime, server_default=sqlalchemy.sql.func.now())
    changedby = UUIDFKey(nullable=True)#Column(ForeignKey("users.id"), index=True, nullable=True)
    createdby = UUIDFKey(nullable=True)#Column(ForeignKey("users.id"), index=True, nullable=True)

