from email.policy import default
import sqlalchemy
import datetime

from sqlalchemy import Column, String, BigInteger, Integer, DateTime, ForeignKey, Sequence, Table, Boolean
from sqlalchemy.dialects.postgresql import UUID

from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

BaseModel = declarative_base()

def UUIDColumn(name=None):
    if name is None:
        return Column(UUID(as_uuid=True), primary_key=True, server_default=sqlalchemy.text("gen_random_uuid()"),)
    else:
        return Column(name, UUID(as_uuid=True), primary_key=True, server_default=sqlalchemy.text("gen_random_uuid()"),)

#id = Column(UUID(as_uuid=True), primary_key=True, server_default=sqlalchemy.text("uuid_generate_v4()"),)

class MembershipModel(BaseModel):
    """Spojuje User s Group jestlize User je clen Group
       Umoznuje udrzovat historii spojeni
    """

    __tablename__ = 'memberships'

    id = UUIDColumn()
    user_id = Column(ForeignKey('users.id'), primary_key=True)
    group_id = Column(ForeignKey('groups.id'), primary_key=True)

    startdate = Column(DateTime)
    enddate = Column(DateTime)
    valid = Column(Boolean, default=True)

    user = relationship('UserModel', back_populates='memberships')
    group = relationship('GroupModel', back_populates='memberships')

class UserModel(BaseModel):
    """Spravuje data spojena s uzivatelem
    """
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

    memberships = relationship('MembershipModel', back_populates='user')
    roles = relationship('RoleModel', back_populates='user')

class GroupModel(BaseModel):
    """Spravuje data spojena se skupinou
    """
    __tablename__ = 'groups'
    
    id = UUIDColumn()
    name = Column(String)
    
    lastchange = Column(DateTime, default=datetime.datetime.now)
    
    startDate = Column(DateTime)
    endDate = Column(DateTime)
    valid = Column(Boolean, default=True)

    externalId = Column(String, index=True)

    grouptype_id = Column(ForeignKey('grouptypes.id'))
    grouptype = relationship('GroupTypeModel', back_populates='groups')

    mastergroup_id = Column(ForeignKey('groups.id'))
    #mastergroup = relationship('GroupModel', back_populates='subgroups', uselist=False, foreign_keys=[mastergroup_id])
    #mastergroup = relationship('GroupModel', uselist=False, foreign_keys=[mastergroup_id])
    #subgroups = relationship('GroupModel', back_populates='mastergroup', uselist=True, foreign_keys=[])

    memberships = relationship('MembershipModel', back_populates='group')
    roles = relationship('RoleModel', back_populates='group')

class GroupTypeModel(BaseModel):
    """Urcuje typ skupiny (fakulta, katedra, studijni skupina apod.)
    """
    __tablename__ = 'grouptypes'
    
    id = UUIDColumn()
    name = Column(String)

    groups = relationship('GroupModel', back_populates='grouptype')

class RoleTypeModel(BaseModel):
    """Urcuje typ role (Vedouci katedry, dekan apod.)
    """
    __tablename__ = 'roletypes'

    id = UUIDColumn()
    name = Column(String)

    roles = relationship('RoleModel', back_populates='roletype')

class RoleModel(BaseModel):
    """Spojuje uzivatele a skupinu, ve ktere uzivatel "hraje" roli 
    """
    __tablename__ = 'roles'

    id = UUIDColumn()
    user_id = Column(ForeignKey('users.id'))
    group_id = Column(ForeignKey('groups.id'))
    roletype_id = Column(ForeignKey('roletypes.id'))

    startdate = Column(DateTime)
    enddate = Column(DateTime)
    valid = Column(Boolean)

    roletype = relationship('RoleTypeModel', back_populates='roles')
    user = relationship('UserModel', back_populates='roles')
    group = relationship('GroupModel', back_populates='roles')


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