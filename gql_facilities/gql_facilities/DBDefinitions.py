from unicodedata import name
import sqlalchemy
import datetime

from sqlalchemy import Column, String, BigInteger, Integer, DateTime, ForeignKey, Sequence, Table, Boolean
from sqlalchemy.dialects.postgresql import UUID

from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

BaseModel = declarative_base()
###

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


""" class MembershipModel(BaseModel):
    """
class FacilityModel(BaseModel):
    """Spravuje data spojena s objektem daneho typu
    """
    __tablename__= 'facilities'

    id = UUIDColumn()
    name = Column(String)
    address = Column(String)
    valid = Column(Boolean, default=True)
    startdate = Column(DateTime)
    enddate = Column(DateTime)
    facilitytype_id = Column(ForeignKey('facilitytypes.id'))
    capacity = Column(Integer)
    manager_id = Column(ForeignKey('users.id'), primary_key=True)
    
    master_facility_id = Column(ForeignKey('facilities.id'), primary_key=True)   
    external_id = Column(String, index=True)

class FacilityTypeModel(BaseModel):
    """Urcuje typ objektu (areal, budova, patro, mistnost)
    """
    __tablename__= 'facilitytypes'
    id=UUIDColumn()
    name=Column(String)

    facilities=relationship('FacilityModel', back_populates='facilitytype')


class UserModel(BaseModel):
    """Spravuje data spojena s uzivatelem
    """
    __tablename__ = 'users'

    id = UUIDColumn()
   # name = Column(String)
    #surname = Column(String)
   
    #externalId = Column(BigInteger, index=True)

   

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