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

class WorkflowStateUserModel(BaseModel):
    """model pristupu - uzivatel + skupina"""

    __tablename__ = "awworkflowstateusers"

    id = UUIDColumn()
    name = Column(String)
    accesslevel = Column(Integer)

    workflowstate_id = Column(ForeignKey("awworkflowstates.id"), index=True)
    #workflowstate = relationship("WorkflowStateModel", back_populates="users")

    user_id = UUIDFKey(nullable=True)#Column(ForeignKey("users.id"), index=True)
    group_id = UUIDFKey(nullable=True)#Column(ForeignKey("groups.id"), index=True)

    created = Column(DateTime, server_default=sqlalchemy.sql.func.now())
    lastchange = Column(DateTime, server_default=sqlalchemy.sql.func.now())
    changedby = UUIDFKey(nullable=True)#Column(ForeignKey("users.id"), index=True, nullable=True)
    createdby = UUIDFKey(nullable=True)#Column(ForeignKey("users.id"), index=True, nullable=True)

