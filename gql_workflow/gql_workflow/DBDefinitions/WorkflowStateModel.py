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

class WorkflowStateModel(BaseModel):
    """stav v posloupnosti (vrchol)"""

    __tablename__ = "awworkflowstates"

    id = UUIDColumn()
    name = Column(String)
    name_en = Column(String)

    valid = Column(Boolean)

    workflow_id = Column(ForeignKey("awworkflows.id"), index=True)
    #workflow = relationship("WorkflowModel", back_populates="states")
    #roletypes = relationship("WorkflowStateRoleModel", back_populates="workflowstate")
    #users = relationship("WorkflowStateUserModel", back_populates="workflowstate")

    created = Column(DateTime, server_default=sqlalchemy.sql.func.now())
    lastchange = Column(DateTime, server_default=sqlalchemy.sql.func.now())
    changedby = UUIDFKey(nullable=True)#Column(ForeignKey("users.id"), index=True, nullable=True)
    createdby = UUIDFKey(nullable=True)#Column(ForeignKey("users.id"), index=True, nullable=True)