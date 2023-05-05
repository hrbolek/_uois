import sqlalchemy
from sqlalchemy.future import select
import datetime

from sqlalchemy import Column, String, BigInteger, Integer, DateTime, ForeignKey, Sequence, Table, Boolean
from sqlalchemy.dialects.postgresql import UUID

from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

BaseModel = declarative_base()

def UUIDColumn(name=None):
    if name is None:
        return Column(UUID(as_uuid=True), primary_key=True, server_default=sqlalchemy.text("gen_random_uuid()"), unique=True)
    else:
        return Column(name, UUID(as_uuid=True), primary_key=True, server_default=sqlalchemy.text("gen_random_uuid()"), unique=True)
    
#id = Column(UUID(as_uuid=True), primary_key=True, server_default=sqlalchemy.text("uuid_generate_v4()"),)

###########################################################################################################################
#
# zde definujte sve SQLAlchemy modely
# je-li treba, muzete definovat modely obsahujici jen id polozku, na ktere se budete odkazovat
#
###########################################################################################################################

class UserModel(BaseModel):
    __tablename__ = "users"

    id = UUIDColumn()
    requests = relationship('RequestModel', back_populates='user')

class RequestModel(BaseModel):
    __tablename__ = "forms"

    id = UUIDColumn()
    name = Column(String)
    creator_id = Column(ForeignKey("users.id"), primary_key=True)
    create_at = Column(DateTime, server_default=sqlalchemy.sql.func.now())
    lastchange  = Column(DateTime, server_default=sqlalchemy.sql.func.now())
    status = Column(String) 

    user = relationship("UserModel", back_populates="requests")
    sections = relationship("SectionModel", back_populates="request")

    
class SectionModel(BaseModel):
    __tablename__ = "formsections"

    id = UUIDColumn()
    name = Column(String)

    request_id = Column(ForeignKey("forms.id"), primary_key=True)
    create_at = Column(DateTime, server_default=sqlalchemy.sql.func.now())
    lastchange  = Column(DateTime, server_default=sqlalchemy.sql.func.now())
    order = Column(Integer)
    status = Column(String)

    request = relationship("RequestModel", back_populates="sections")
    parts = relationship("PartModel", back_populates="section")
    

class PartModel(BaseModel):
    __tablename__ = "formparts"
    
    id = UUIDColumn()
    name = Column(String)

    create_at = Column(DateTime, server_default=sqlalchemy.sql.func.now())
    lastchange  = Column(DateTime, server_default=sqlalchemy.sql.func.now())
    order = Column(Integer)

    section_id = Column(ForeignKey("formsections.id"), primary_key=True)
    section = relationship("SectionModel", back_populates="parts")
    items = relationship("ItemModel", back_populates="part")
    
class ItemModel(BaseModel):
    __tablename__ = "formitems"

    id = UUIDColumn()
    name = Column(String)

    create_at = Column(DateTime, server_default=sqlalchemy.sql.func.now())
    lastchange  = Column(DateTime, server_default=sqlalchemy.sql.func.now())
    order = Column(Integer)

    value = Column(String)

    part_id = Column(ForeignKey("formparts.id"), primary_key=True)
    part = relationship("PartModel", back_populates="items")



###########################################################################################################################

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.ext.asyncio import create_async_engine

async def startEngine(connectionstring, makeDrop=False, makeUp=True):
    """Provede nezbytne ukony a vrati asynchronni SessionMaker """
    asyncEngine = create_async_engine(connectionstring) 

    async with asyncEngine.begin() as conn:
        if makeDrop:
            await conn.run_sync(BaseModel.metadata.drop_all)
            print('BaseModel.metadata.drop_all finished')
        if makeUp:
            try:
                await conn.run_sync(BaseModel.metadata.create_all)    
                print('BaseModel.metadata.create_all finished')
            except sqlalchemy.exc.NoReferencedTableError as e:
                print(e)
                print('Unable automaticaly create tables')
                return None

    async_sessionMaker = sessionmaker(
        asyncEngine, expire_on_commit=False, class_=AsyncSession
    )
    return async_sessionMaker




import os
def ComposeConnectionString():
    """Odvozuje connectionString z promennych prostredi (nebo z Docker Envs, coz je fakticky totez).
       Lze predelat na napr. konfiguracni file.
    """
    user = os.environ.get("POSTGRES_USER", "postgres")
    password = os.environ.get("POSTGRES_PASSWORD", "example")
    database =  os.environ.get("POSTGRES_DB", "data")
    hostWithPort =  os.environ.get("POSTGRES_HOST", "postgres:5432")
    
    driver = "postgresql+asyncpg" #"postgresql+psycopg2"
    connectionstring = f"{driver}://{user}:{password}@{hostWithPort}/{database}"

    return connectionstring