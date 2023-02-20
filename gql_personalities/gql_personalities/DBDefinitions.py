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

###########################################################################################################################
#
# zde definujte sve SQLAlchemy modely
# je-li treba, muzete definovat modely obsahujici jen id polozku, na ktere se budete odkazovat
#
###########################################################################################################################

class RankModel(BaseModel):
    __tablename__ = "personalitiesranks"

    id = UUIDColumn()
    start = Column(DateTime)
    end = Column(DateTime)

    user_id = UUIDFKey(nullable=True)#Column(ForeignKey("users.id"), index=True)
    rankType_id = Column(ForeignKey("personalitiesranktypes.id"), index=True)

    created = Column(DateTime, server_default=sqlalchemy.sql.func.now())
    lastchange = Column(DateTime, server_default=sqlalchemy.sql.func.now())
    changedby = UUIDFKey(nullable=True)#Column(ForeignKey("users.id"), index=True, nullable=True)
    changedby = UUIDFKey(nullable=True)#Column(ForeignKey("users.id"), index=True, nullable=True)


    #user = relationship("UserModel", back_populates="ranks", foreign_keys=[user_id])
    rankType = relationship("RankTypeModel", back_populates="rank")


class RankTypeModel(BaseModel):
    __tablename__ = "personalitiesranktypes"

    id = UUIDColumn()
    name = Column(String)
    name_en = Column(String)

    created = Column(DateTime, server_default=sqlalchemy.sql.func.now())
    lastchange = Column(DateTime, server_default=sqlalchemy.sql.func.now())
    changedby = UUIDFKey(nullable=True)#Column(ForeignKey("users.id"), index=True, nullable=True)
    changedby = UUIDFKey(nullable=True)#Column(ForeignKey("users.id"), index=True, nullable=True)

    rank = relationship("RankModel", back_populates="rankType")


class StudyModel(BaseModel):
    __tablename__ = "personalitiesstudies"

    id = UUIDColumn()
    name = Column(String)
    name_en = Column(String)
    program = Column(String)
    start = Column(DateTime)
    end = Column(DateTime)

    user_id = UUIDFKey(nullable=True)#Column(ForeignKey("users.id"), index=True)

    created = Column(DateTime, server_default=sqlalchemy.sql.func.now())
    lastchange = Column(DateTime, server_default=sqlalchemy.sql.func.now())
    changedby = UUIDFKey(nullable=True)#Column(ForeignKey("users.id"), index=True, nullable=True)
    changedby = UUIDFKey(nullable=True)#Column(ForeignKey("users.id"), index=True, nullable=True)

    #user = relationship("UserModel", back_populates="studies", foreign_keys=[user_id])


class CertificateModel(BaseModel):
    __tablename__ = "personalitiescertificates"

    id = UUIDColumn()
    level = Column(String)
    validity_start = Column(DateTime)
    validity_end = Column(DateTime)

    user_id = UUIDFKey(nullable=True)#Column(ForeignKey("users.id"), index=True)
    certificateType_id = Column(ForeignKey("personalitiescertificatetypes.id"), index=True)

    created = Column(DateTime, server_default=sqlalchemy.sql.func.now())
    lastchange = Column(DateTime, server_default=sqlalchemy.sql.func.now())
    changedby = UUIDFKey(nullable=True)#Column(ForeignKey("users.id"), index=True, nullable=True)
    changedby = UUIDFKey(nullable=True)#Column(ForeignKey("users.id"), index=True, nullable=True)

    #user = relationship("UserModel", back_populates="certificates", foreign_keys=[user_id])
    certificateType = relationship("CertificateTypeModel", back_populates="certificates")


class CertificateTypeModel(BaseModel):
    __tablename__ = "personalitiescertificatetypes"

    id = UUIDColumn()
    name = Column(String)
    name_en = Column(String)

    certificateTypeGroup_id = Column(
        ForeignKey("personalitiescertificatecategories.id")
    )

    certificates = relationship("CertificateModel", back_populates="certificateType")
    certificateTypeGroup = relationship(
        "CertificateTypeGroupModel", back_populates="certificateType"
    )

    created = Column(DateTime, server_default=sqlalchemy.sql.func.now())
    lastchange = Column(DateTime, server_default=sqlalchemy.sql.func.now())
    changedby = UUIDFKey(nullable=True)#Column(ForeignKey("users.id"), index=True, nullable=True)
    changedby = UUIDFKey(nullable=True)#Column(ForeignKey("users.id"), index=True, nullable=True)

class CertificateTypeGroupModel(BaseModel):
    __tablename__ = "personalitiescertificatecategories"

    id = UUIDColumn()
    name = Column(String)
    name_en = Column(String)

    created = Column(DateTime, server_default=sqlalchemy.sql.func.now())
    lastchange = Column(DateTime, server_default=sqlalchemy.sql.func.now())
    changedby = UUIDFKey(nullable=True)#Column(ForeignKey("users.id"), index=True, nullable=True)
    changedby = UUIDFKey(nullable=True)#Column(ForeignKey("users.id"), index=True, nullable=True)

    certificateType = relationship(
        "CertificateTypeModel", back_populates="certificateTypeGroup"
    )


class MedalModel(BaseModel):
    __tablename__ = "personalitiesmedals"

    id = UUIDColumn()
    year = Column(Integer)

    user_id = UUIDFKey(nullable=True)#Column(ForeignKey("users.id"), index=True)
    medalType_id = Column(ForeignKey("personalitiesmedaltypes.id"), index=True)

    created = Column(DateTime, server_default=sqlalchemy.sql.func.now())
    lastchange = Column(DateTime, server_default=sqlalchemy.sql.func.now())
    changedby = UUIDFKey(nullable=True)#Column(ForeignKey("users.id"), index=True, nullable=True)
    changedby = UUIDFKey(nullable=True)#Column(ForeignKey("users.id"), index=True, nullable=True)

    #user = relationship("UserModel", back_populates="medals", foreign_keys=[user_id])
    medalType = relationship("MedalTypeModel", back_populates="medal")


class MedalTypeModel(BaseModel):
    __tablename__ = "personalitiesmedaltypes"

    id = UUIDColumn()
    name = Column(String)
    name_en = Column(String)

    medalTypeGroup_id = Column(ForeignKey("personalitiesmedalcategories.id"), index=True)

    created = Column(DateTime, server_default=sqlalchemy.sql.func.now())
    lastchange = Column(DateTime, server_default=sqlalchemy.sql.func.now())
    changedby = UUIDFKey(nullable=True)#Column(ForeignKey("users.id"), index=True, nullable=True)
    changedby = UUIDFKey(nullable=True)#Column(ForeignKey("users.id"), index=True, nullable=True)

    medal = relationship("MedalModel", back_populates="medalType")
    medalTypeGroup = relationship("MedalTypeGroupModel", back_populates="medalTypes")


class MedalTypeGroupModel(BaseModel):
    __tablename__ = "personalitiesmedalcategories"

    id = UUIDColumn()
    name = Column(String)
    name_en = Column(String)

    created = Column(DateTime, server_default=sqlalchemy.sql.func.now())
    lastchange = Column(DateTime, server_default=sqlalchemy.sql.func.now())
    changedby = UUIDFKey(nullable=True)#Column(ForeignKey("users.id"), index=True, nullable=True)
    changedby = UUIDFKey(nullable=True)#Column(ForeignKey("users.id"), index=True, nullable=True)

    medalTypes = relationship("MedalTypeModel", back_populates="medalTypeGroup")


class WorkHistoryModel(BaseModel):
    __tablename__ = "personalitiesworkhistories"

    id = UUIDColumn()
    start = Column(DateTime)
    end = Column(DateTime)
    name = Column(String)
    ico = Column(String)

    user_id = UUIDFKey(nullable=True)#Column(ForeignKey("users.id"))

    created = Column(DateTime, server_default=sqlalchemy.sql.func.now())
    lastchange = Column(DateTime, server_default=sqlalchemy.sql.func.now())
    changedby = UUIDFKey(nullable=True)#Column(ForeignKey("users.id"), index=True, nullable=True)
    changedby = UUIDFKey(nullable=True)#Column(ForeignKey("users.id"), index=True, nullable=True)

    #user = relationship("UserModel", back_populates="workHistories", foreign_keys=[user_id])


class RelatedDocModel(BaseModel):
    __tablename__ = "personalitiesrelateddocs"

    id = UUIDColumn()
    name = Column(String)
    # doc_upload

    user_id = UUIDFKey(nullable=True)#Column(ForeignKey("users.id"))

    created = Column(DateTime, server_default=sqlalchemy.sql.func.now())
    lastchange = Column(DateTime, server_default=sqlalchemy.sql.func.now())
    changedby = UUIDFKey(nullable=True)#Column(ForeignKey("users.id"), index=True, nullable=True)
    changedby = UUIDFKey(nullable=True)#Column(ForeignKey("users.id"), index=True, nullable=True)

    #user = relationship("UserModel", back_populates="relatedDocs", foreign_keys=[user_id])


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
