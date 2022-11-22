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
    #name = Column(String)
    #surname = Column(String)
    #email = Column(String)
    #valid = Column(Boolean, default=True)
    #startdate = Column(DateTime)
    #enddate = Column(DateTime)
    
    #lastchange = Column(DateTime, default=datetime.datetime.now)
    #externalId = Column(BigInteger, index=True)

    ranks = relationship('rank_history', back_populates='user')
    studies = relationship('study', back_populates='user')
    certificates = relationship('certificate', back_populates='user')
    medals = relationship('medal', back_populates='user')
    work_histories = relationship('work_history', back_populates='user')
    related_docs = relationship('related_doc', back_populates='user')

class rank_history(BaseModel):
    __tablename__ = 'ranks'

    id = UUIDColumn()
    rank_from = Column(int)
    rank_until = Column(Integer) ###kunzultovat Int/Integer
    rank_name = Column(String)
    
    user = relationship('UserModel', back_populates = 'rank_history')

class study(BaseModel):
    __tablename__ = 'studies'

    id = UUIDColumn()
    study_place = Column(String)
    study_from = Column(int)
    study_until = Column(int)
    study_program = Column(String)
    
    user = relationship('UserModel', back_populates = 'study') ### konzultovat název

class certificate(BaseModel):
    __tablename__ = 'certficates'

    id = UUIDColumn()
    certificate_level = Column(String)
    certificate_name = Column(String)
    certificate_validity_from = Column(int)
    certificate_validity_until = Column(int)
    
    user = relationship('UserModel', back_populates = 'certificate')
    certificate_type = relationship('certificate_type', back_populates = 'certificate')

class certificate_type(BaseModel):
    __tablename__ = 'certificate_types'

    id = UUIDColumn()
    certificate_type_kind = Column(String)
    
    certificates = relationship('certificate', back_populates = 'certificate_type')

class medal(BaseModel):
    __tablename__ = 'medals'

    id = UUIDColumn()
    medal_year = Column(int)
    medal_name = Column(String)
    
    user = relationship('UserModel', back_populates = 'medal')
    medal_type = relationship('medal_type', back_populates = 'medal')

class medal_type(BaseModel):
    __tablename__ = 'medal_types'

    id = UUIDColumn()
    medal_type_kind = Column(String)
    
    medals = relationship('medal', back_populates = 'medal_type')

class work_history(BaseModel):
    __tablename__ = 'work_histories'

    id = UUIDColumn()
    work_from = Column(int)
    work_until = Column(int)
    work_position = Column(String)
    work_ico = Column(String)
    
    user = relationship('UserModel', back_populates = 'work_history')

class related_doc(BaseModel):
    __tablename__ = 'related_docs'

    id = UUIDColumn()
    doc_name = Column(String)
    
    user = relationship('UserModel', back_populates = 'related_doc')



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