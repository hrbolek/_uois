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
    Date,
    Float,
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

###########################################################################################################################
#
# zde definujte sve SQLAlchemy modely
# je-li treba, muzete definovat modely obsahujici jen id polozku, na ktere se budete odkazovat
#
###########################################################################################################################


class PlanSubjectModel(BaseModel):
    """Spravuje data spojena s predmetem"""

    __tablename__ = "plan_subjects"

    id = UUIDColumn()


class SubjectModel(BaseModel):
    """Spojujici tabulka - predmet, publikace"""

    __tablename__ = "publication_subjects"

    id = UUIDColumn()
    publication_id = Column(ForeignKey("publications.id"), index=True)
    subject_id = UUIDFKey(nullable=True)#Column(ForeignKey("plan_subjects.id"), index=True)

    #publication = relationship("PublicationModel")
    #subject = relationship("PlanSubjectModel")

    created = Column(DateTime, server_default=sqlalchemy.sql.func.now())
    lastchange = Column(DateTime, server_default=sqlalchemy.sql.func.now())
    createdby = UUIDFKey(nullable=True)#Column(ForeignKey("users.id"), index=True, nullable=True)
    changedby = UUIDFKey(nullable=True)#Column(ForeignKey("users.id"), index=True, nullable=True)

class PublicationModel(BaseModel):

    __tablename__ = "publications"

    id = UUIDColumn()
    name = Column(String)

    publication_type_id = Column(ForeignKey("publicationtypes.id"), index=True)
    place = Column(String)
    published_date = Column(Date)
    reference = Column(String)
    valid = Column(Boolean)

    created = Column(DateTime, server_default=sqlalchemy.sql.func.now())
    lastchange = Column(DateTime, server_default=sqlalchemy.sql.func.now())
    createdby = UUIDFKey(nullable=True)#Column(ForeignKey("users.id"), index=True, nullable=True)
    changedby = UUIDFKey(nullable=True)#Column(ForeignKey("users.id"), index=True, nullable=True)

    #author = relationship("AuthorModel", back_populates="publication")
    #publication_type = relationship(
    #    "PublicationTypeModel", back_populates="publication"
    #)


class AuthorModel(BaseModel):
    __tablename__ = "publication_authors"

    id = UUIDColumn()
    user_id = UUIDFKey(nullable=True)#Column(ForeignKey("users.id"), index=True)
    publication_id = Column(ForeignKey("publications.id"), index=True)
    order = Column(Integer)
    share = Column(Float)

    #user = relationship("UserModel", back_populates="author")
    #publication = relationship("PublicationModel", back_populates="author")

    created = Column(DateTime, server_default=sqlalchemy.sql.func.now())
    lastchange = Column(DateTime, server_default=sqlalchemy.sql.func.now())
    createdby = UUIDFKey(nullable=True)#Column(ForeignKey("users.id"), index=True, nullable=True)
    changedby = UUIDFKey(nullable=True)#Column(ForeignKey("users.id"), index=True, nullable=True)

class PublicationTypeModel(BaseModel):
    __tablename__ = "publicationtypes"

    id = UUIDColumn()
    name = Column(String)
    name_en = Column(String)

    category_id = Column(ForeignKey("publicationcategories.id"), index=True, nullable=True)
    #publication = relationship("PublicationModel", back_populates="publication_type")

    created = Column(DateTime, server_default=sqlalchemy.sql.func.now())
    lastchange = Column(DateTime, server_default=sqlalchemy.sql.func.now())
    createdby = UUIDFKey(nullable=True)#Column(ForeignKey("users.id"), index=True, nullable=True)
    changedby = UUIDFKey(nullable=True)#Column(ForeignKey("users.id"), index=True, nullable=True)

class PublicationCategoryModel(BaseModel):
    __tablename__ = "publicationcategories"

    id = UUIDColumn()
    name = Column(String)
    name_en = Column(String)

    created = Column(DateTime, server_default=sqlalchemy.sql.func.now())
    lastchange = Column(DateTime, server_default=sqlalchemy.sql.func.now())
    createdby = UUIDFKey(nullable=True)#Column(ForeignKey("users.id"), index=True, nullable=True)
    changedby = UUIDFKey(nullable=True)#Column(ForeignKey("users.id"), index=True, nullable=True)

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
