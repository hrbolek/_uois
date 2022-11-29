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

    ranks = relationship('Rank', back_populates='user')
    studies = relationship('Study', back_populates='user')
    certificates = relationship('Certificate', back_populates='user')
    medals = relationship('Medal', back_populates='user')
    workHistories = relationship('WorkHistory', back_populates='user')
    relatedDocs = relationship('RelatedDoc', back_populates='user')

class Rank(BaseModel):
    __tablename__ = 'personalitiesRanks'

    id = UUIDColumn()
    start = Column(DateTime)
    end = Column(DateTime) 

    user_id = Column(ForeignKey('users.id'))
    rankType_id = Column(ForeignKey('personalitiesRankTypes.id'))

    user = relationship('UserModel', back_populates = 'Rank')
    rankType = relationship('RankType', back_populates = 'Rank')

class RankType(BaseModel):
    __tablename__ = 'personalitiesRankTypes'

    id = UUIDColumn()
    name = Column(String)

    rank = relationship('Rank', back_populates = 'RankTypes')

class Study(BaseModel):
    __tablename__ = 'personalitiesStudies'

    id = UUIDColumn()
    place = Column(String)
    program = Column(String)
    start = Column(DateTime)
    end = Column(DateTime)
    
    user_id = Column(ForeignKey('users.id'))
    
    user = relationship('UserModel', back_populates = 'Study')

class Certificate(BaseModel):
    __tablename__ = 'personalitiesCertificates'

    id = UUIDColumn()
    level = Column(String)
    validity_start = Column(DateTime)
    validity_end = Column(DateTime)

    user_id = Column(ForeignKey('users.id'))
    certificateType_id = Column(ForeignKey('personalitiesCertificateTypes.id'))
    
    user = relationship('UserModel', back_populates = 'Certificate')
    certificateType = relationship('CertificateType', back_populates = 'Certificate')

class CertificateType(BaseModel):
    __tablename__ = 'personalitiesCertificateTypes'

    id = UUIDColumn()
    name = Column(String)
    
    certificate = relationship('Certificate', back_populates = 'CertificateType')

class Medal(BaseModel):
    __tablename__ = 'personalitiesMedals'

    id = UUIDColumn()
    year = Column(Integer)
    
    user_id = Column(ForeignKey('users.id'))
    medalType_id = Column(ForeignKey('personalitiesMedalTypes.id'))
    
    user = relationship('UserModel', back_populates = 'Medal')
    medalType = relationship('MedalType', back_populates = 'Medal')

class MedalType(BaseModel):
    __tablename__ = 'personalitiesMedalTypes'

    id = UUIDColumn()
    name = Column(String)
    
    medalTypeGroup_id = Column(ForeignKey('personalitiesMedalTypeGroups.id'))

    medal = relationship('Medal', back_populates = 'MedalType')
    medalTypeGroup = relationship('MedalTypeGroup', back_populates = 'MedalType')

class MedalTypeGroup(BaseModel):
    __tablename__ = 'personalitiesMedalTypeGroups'

    id = UUIDColumn()
    name = Column(String)
    
    medalType = relationship('MedalType', back_populates = 'MedalTypeGroup')

class WorkHistory(BaseModel):
    __tablename__ = 'personalitiesWorkHistories'

    id = UUIDColumn()
    start = Column(DateTime)
    end = Column(DateTime)
    position = Column(String)
    ico = Column(String)

    user_id = Column(ForeignKey('users.id'))
    
    user = relationship('UserModel', back_populates = 'WorkHistory')

class RelatedDoc(BaseModel):
    __tablename__ = 'personalitiesRelatedDocs'

    id = UUIDColumn()
    name = Column(String)
    #saved ? (destination?)

    user_id = Column(ForeignKey('users.id'))
    
    user = relationship('UserModel', back_populates = 'RelatedDoc')



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