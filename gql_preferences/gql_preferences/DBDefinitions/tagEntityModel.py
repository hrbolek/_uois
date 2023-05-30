import sqlalchemy
from sqlalchemy import Column, String, BigInteger, Integer, DateTime, ForeignKey, Sequence, Table, Boolean, Float, DECIMAL
from uoishelpers.uuid import UUIDColumn
from .Base import BaseModel, UUIDFKey

class TagEntityModel(BaseModel):
    __tablename__ = "preferedtagentities"
    id = UUIDColumn(postgres=False)

    author_id = UUIDFKey(nullable=True)#Column(ForeignKey("users.id"), index=True, nullable=True)
    tag_id = Column(ForeignKey("preferedtags.id"), index=True, nullable=True)
    entity_id = UUIDFKey(nullable=True)#Column(ForeignKey("users.id"), index=True, nullable=True)
    entity_type_id = UUIDFKey(nullable=True)#Column(ForeignKey("users.id"), index=True, nullable=True)

    created = Column(DateTime, server_default=sqlalchemy.sql.func.now())
    lastchange = Column(DateTime, server_default=sqlalchemy.sql.func.now())
    
    createdby = UUIDFKey(nullable=True)#Column(ForeignKey("users.id"), index=True, nullable=True)
    changedby = UUIDFKey(nullable=True)#Column(ForeignKey("users.id"), index=True, nullable=True)
