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

class UserModel(BaseModel):
    """uzivatele v minimalni definici
    """
    __tablename__ = 'users'
    id = UUIDColumn()

class GroupModel(BaseModel):
    """skupiny v minimalni definici
    """
    __tablename__ = 'groups'
    id = UUIDColumn()

class RoleTypeModel(BaseModel):
    ""
    __tablename__ = 'roletypes'
    id = UUIDColumn()

class AuthorizationModel(BaseModel):
    """Spravuje pristupove informace
    """
    __tablename__ = 'authorizations'

    id = UUIDColumn()
    workflow = relationship('WorkflowModel', back_populates='authorization')
    useraccesses = relationship('AuthorizationUserModel', back_populates='authorization')
    groupaccesses = relationship('AuthorizationGroupModel', back_populates='authorization')
    roletypeacesses = relationship('AuthorizationRoleTypeModel', back_populates='authorization')

class AuthorizationUserModel(BaseModel):
    """Spravuje pristupove informace zalozene na uzivatelich
    """
    __tablename__ = 'authorizationusers'

    id = UUIDColumn()
    authorization_id = Column(ForeignKey('authorizations.id'), primary_key=True)
    authorization = relationship('AuthorizationModel', back_populates='useraccesses')
    user_id = Column(ForeignKey('users.id'), primary_key=True)
    accesslevel = Column(Integer)

class AuthorizationGroupModel(BaseModel):
    """Spravuje pristupove informace zalozene na skupinach
    """
    __tablename__ = 'authorizationgroups'

    id = UUIDColumn()
    authorization_id = Column(ForeignKey('authorizations.id'), primary_key=True)
    authorization = relationship('AuthorizationModel', back_populates='groupaccesses')
    group_id = Column(ForeignKey('groups.id'), primary_key=True)
    accesslevel = Column(Integer)

class AuthorizationRoleTypeModel(BaseModel):
    """Spravuje pristupove informace zalozene na rolich ve skupinach
    """
    __tablename__ = 'authorizationroletypes'

    id = UUIDColumn()
    authorization_id = Column(ForeignKey('authorizations.id'), primary_key=True)
    authorization = relationship('AuthorizationModel', back_populates='roletypeacesses')
    roletype_id = Column(ForeignKey('roletypes.id'), primary_key=True)
    accesslevel = Column(Integer)

class WorkflowModel(BaseModel):
    """Posloupnost stavu a moznosti prechodu mezi nimi (graf)
    """

    __tablename__ = 'workflows'

    id = UUIDColumn()
    name = Column(String)

    authorization_id = Column(ForeignKey('authorizations.id'), primary_key=True)
    authorization = relationship('AuthorizationModel', back_populates='workflow')

    states = relationship('WorkflowStateModel', back_populates='workflow')

class WorkflowStateModel(BaseModel):
    """stav v posloupnosti (vrchol)
    """
    __tablename__ = 'workflowstates'

    id = UUIDColumn()
    name = Column(String)
    
    workflow_id = Column(ForeignKey('workflows.id'), primary_key=True)
    workflow = relationship('WorkflowModel', back_populates='states')
    roletypes = relationship('WorkflowStateRoleModel', back_populates='workflowstate')
    users = relationship('WorkflowStateUserModel', back_populates='workflowstate')

class WorkflowStateRoleTypeModel(BaseModel):
    """model pristupu - role, kterou musi splnovat
    """
    __tablename__ = 'workflowstateroletypes'

    id = UUIDColumn()
    name = Column(String)
    accesslevel = Column(Integer)

    workflowstate_id = Column(ForeignKey('workflowstates.id'), primary_key=True)
    workflowstate = relationship('WorkflowStateModel', back_populates='roletypes')

    roletype_id = Column(ForeignKey('roletypes.id'), primary_key=True)

class WorkflowStateUserModel(BaseModel):
    """model pristupu - uzivatel + skupina
    """
    __tablename__ = 'workflowstateusers'

    id = UUIDColumn()
    name = Column(String)
    accesslevel = Column(Integer)
    
    workflowstate_id = Column(ForeignKey('workflowstates.id'), primary_key=True)
    workflowstate = relationship('WorkflowStateModel', back_populates='users')

    user_id = Column(ForeignKey('users.id'), primary_key=True)

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