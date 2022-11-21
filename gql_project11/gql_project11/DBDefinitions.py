import sqlalchemy
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
    __tablename__ = 'users'

    id = UUIDColumn()
    name = Column(String)
    surname = Column(String)
    email = Column(String)
    valid = Column(Boolean, default=True)
    startdate = Column(DateTime)
    enddate = Column(DateTime)
    
    lastchange = Column(DateTime, default=datetime.datetime.now)
    externalId = Column(BigInteger, index=True)

    #relationships

class rank_history(BaseModel):
    id = UUIDColumn()
    rank_from = Column(int)
    rank_until = Column(Integer) ###kunzultovat Int/Integer
    rank_name = Column(String)
    #relationships

class study(BaseModel):
    id = UUIDColumn()
    study_place = Column(String)
    study_from = Column(int)
    study_until = Column(int)
    study_program = Column(String)
    #relationships

class certificate(BaseModel):
    id = UUIDColumn()
    certificate_level = Column(String)
    certificate_name = Column(String)
    certificate_validity_from = Column(int)
    certificate_validity_until = Column(int)
    #relationships

class certificate_types(BaseModel):
    id = UUIDColumn()
    certificate_types_kind = Column(String)
    #relationships

class medal(BaseModel):
    id = UUIDColumn()
    medal_year = Column(int)
    medal_name = Column(String)
    #relationships

class medal_types(BaseModel):
    id = UUIDColumn()
    medal_types_kind = Column(String)
    #relationships

class work_history(BaseModel):
    id = UUIDColumn()
    work_from = Column(int)
    work_until = Column(int)
    work_position = Column(String)
    work_ico = Column(String)
    #relationships

class related_docs(BaseModel):
    id = UUIDColumn()
    doc_name = Column(String)
    #relationships



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
            await conn.run_sync(BaseModel.metadata.create_all)    
            print('BaseModel.metadata.create_all finished')

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