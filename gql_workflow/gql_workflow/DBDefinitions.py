import sqlalchemy
import datetime

from sqlalchemy import (
    Column,
    String,
    BigInteger,
    Integer,
    DateTime,
    ForeignKey,
    Sequence,
    Table,
    Boolean,
)
from sqlalchemy.dialects.postgresql import UUID

from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
import uuid

BaseModel = declarative_base()

def newUuidAsString():
    return f"{uuid.uuid1()}"


def UUIDColumn(name=None):
    if name is None:
        return Column(String, primary_key=True, unique=True, default=newUuidAsString)
    else:
        return Column(
            name, String, primary_key=True, unique=True, default=newUuidAsString
        )

def UUIDFKey(*, ForeignKey=None, nullable=False):
    if ForeignKey is None:
        return Column(
            String, index=True, nullable=nullable
        )
    else:
        return Column(
            ForeignKey, index=True, nullable=nullable
        )
# id = Column(UUID(as_uuid=True), primary_key=True, server_default=sqlalchemy.text("uuid_generate_v4()"),)

class AuthorizationModel(BaseModel):
    """Spravuje pristupove informace"""

    __tablename__ = "awauthorizations"

    id = UUIDColumn()
    #workflow = relationship("WorkflowModel", back_populates="authorization")
    #useraccesses = relationship("AuthorizationUserModel", back_populates="authorization")
    #groupaccesses = relationship("AuthorizationGroupModel", back_populates="authorization")
    #roletypeacesses = relationship("AuthorizationRoleTypeModel", back_populates="authorization")


class AuthorizationUserModel(BaseModel):
    """Spravuje pristupove informace zalozene na uzivatelich"""

    __tablename__ = "awauthorizationusers"

    id = UUIDColumn()
    authorization_id = Column(ForeignKey("awauthorizations.id"), index=True)
    #authorization = relationship("AuthorizationModel", back_populates="useraccesses")
    user_id = UUIDFKey(nullable=True)#Column(ForeignKey("users.id"), index=True)
    accesslevel = Column(Integer)

    created = Column(DateTime, server_default=sqlalchemy.sql.func.now())
    lastchange = Column(DateTime, server_default=sqlalchemy.sql.func.now())
    changedby = UUIDFKey(nullable=True)#Column(ForeignKey("users.id"), index=True, nullable=True)
    createdby = UUIDFKey(nullable=True)#Column(ForeignKey("users.id"), index=True, nullable=True)



class AuthorizationGroupModel(BaseModel):
    """Spravuje pristupove informace zalozene na skupinach"""

    __tablename__ = "awauthorizationgroups"

    id = UUIDColumn()
    authorization_id = Column(ForeignKey("awauthorizations.id"), index=True)
    #authorization = relationship("AuthorizationModel", back_populates="groupaccesses")
    group_id = UUIDFKey(nullable=True)#Column(ForeignKey("groups.id"), index=True)
    accesslevel = Column(Integer)

    created = Column(DateTime, server_default=sqlalchemy.sql.func.now())
    lastchange = Column(DateTime, server_default=sqlalchemy.sql.func.now())
    changedby = UUIDFKey(nullable=True)#Column(ForeignKey("users.id"), index=True, nullable=True)
    createdby = UUIDFKey(nullable=True)#Column(ForeignKey("users.id"), index=True, nullable=True)


class AuthorizationRoleTypeModel(BaseModel):
    """Spravuje pristupove informace zalozene na rolich ve skupinach"""

    __tablename__ = "awauthorizationroletypes"

    id = UUIDColumn()
    authorization_id = Column(ForeignKey("awauthorizations.id"), index=True)
    #authorization = relationship("AuthorizationModel", back_populates="roletypeacesses")
    group_id = UUIDFKey(nullable=True)#ForeignKey("groups.id"), index=True)
    roletype_id = UUIDFKey(nullable=True)#Column(ForeignKey("roletypes.id"), index=True)
    accesslevel = Column(Integer)

    created = Column(DateTime, server_default=sqlalchemy.sql.func.now())
    lastchange = Column(DateTime, server_default=sqlalchemy.sql.func.now())
    changedby = UUIDFKey(nullable=True)#Column(ForeignKey("users.id"), index=True, nullable=True)
    createdby = UUIDFKey(nullable=True)#Column(ForeignKey("users.id"), index=True, nullable=True)


class WorkflowModel(BaseModel):
    """Posloupnost stavu a moznosti prechodu mezi nimi (graf)"""

    __tablename__ = "awworkflows"

    id = UUIDColumn()
    name = Column(String)
    name_en = Column(String)

    authorization_id = Column(ForeignKey("awauthorizations.id"), index=True)
    #authorization = relationship("AuthorizationModel", back_populates="workflow")

    #states = relationship("WorkflowStateModel", back_populates="workflow")

    created = Column(DateTime, server_default=sqlalchemy.sql.func.now())
    lastchange = Column(DateTime, server_default=sqlalchemy.sql.func.now())
    changedby = UUIDFKey(nullable=True)#Column(ForeignKey("users.id"), index=True, nullable=True)
    createdby = UUIDFKey(nullable=True)#Column(ForeignKey("users.id"), index=True, nullable=True)



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

class WorkflowTransitionModel(BaseModel):
    """zmena stav - prechod (hrana)"""

    __tablename__ = "awworkflowtransitions"

    id = UUIDColumn()
    name = Column(String)
    name_en = Column(String)
    valid = Column(Boolean)
    
    workflow_id = Column(ForeignKey("awworkflows.id"), index=True)
    sourcestate_id = Column(ForeignKey("awworkflowstates.id"), index=True)
    destinationstate_id = Column(ForeignKey("awworkflowstates.id"), index=True)

    created = Column(DateTime, server_default=sqlalchemy.sql.func.now())
    lastchange = Column(DateTime, server_default=sqlalchemy.sql.func.now())
    changedby = UUIDFKey(nullable=True)#Column(ForeignKey("users.id"), index=True, nullable=True)
    createdby = UUIDFKey(nullable=True)#Column(ForeignKey("users.id"), index=True, nullable=True)


class WorkflowStateRoleTypeModel(BaseModel):
    """model pristupu - role, kterou musi splnovat"""

    __tablename__ = "awworkflowstateroletypes"

    id = UUIDColumn()
    name = Column(String)
    accesslevel = Column(Integer)

    workflowstate_id = Column(ForeignKey("awworkflowstates.id"), index=True)
    #workflowstate = relationship("WorkflowStateModel", back_populates="roletypes")

    roletype_id = UUIDFKey(nullable=True)#Column(ForeignKey("roletypes.id"), index=True)

    created = Column(DateTime, server_default=sqlalchemy.sql.func.now())
    lastchange = Column(DateTime, server_default=sqlalchemy.sql.func.now())
    changedby = UUIDFKey(nullable=True)#Column(ForeignKey("users.id"), index=True, nullable=True)
    createdby = UUIDFKey(nullable=True)#Column(ForeignKey("users.id"), index=True, nullable=True)


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


from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.ext.asyncio import create_async_engine


async def startEngine(connectionstring, makeDrop=False, makeUp=True):
    """Provede nezbytne ukony a vrati asynchronni SessionMaker"""
    asyncEngine = create_async_engine(connectionstring)

    async with asyncEngine.begin() as conn:
        if makeDrop:
            await conn.run_sync(BaseModel.metadata.drop_all)
            print("BaseModel.metadata.drop_all finished")
        if makeUp:
            try:
                await conn.run_sync(BaseModel.metadata.create_all)
                print("BaseModel.metadata.create_all finished")
            except sqlalchemy.exc.NoReferencedTableError as e:
                print(e)
                print("Unable automaticaly create tables")
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
    database = os.environ.get("POSTGRES_DB", "data")
    hostWithPort = os.environ.get("POSTGRES_HOST", "postgres:5432")

    driver = "postgresql+asyncpg"  # "postgresql+psycopg2"
    connectionstring = f"{driver}://{user}:{password}@{hostWithPort}/{database}"

    return connectionstring
