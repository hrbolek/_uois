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



# id = Column(UUID(as_uuid=True), primary_key=True, server_default=sqlalchemy.text("uuid_generate_v4()"),)

###########################################################################################################################
#
# zde definujte sve SQLAlchemy modely
# je-li treba, muzete definovat modely obsahujici jen id polozku, na ktere se budete odkazovat
#


class GroupModel(BaseModel):
    __tablename__ = "groups"
    id = UUIDColumn()

class UserModel(BaseModel):
    __tablename__ = "users"
    id = UUIDColumn()


class ProgramGroupModel(BaseModel):
    """link a program or a subject to a group of grants"""

    __tablename__ = "acprogramgroups"
    id = UUIDColumn()
    ac_id = (
        UUIDColumn()
    )  # can be a program, also can be a subject, this row can be in a table only once per program and once per subject
    group_id = Column(ForeignKey("groups.id"))


class ProgramFormTypeModel(BaseModel):
    __tablename__ = "acprogramforms"
    id = UUIDColumn()
    name = Column(String)
    name_en = Column(String)
    # present, distant, hybrid

    created = Column(DateTime, server_default=sqlalchemy.sql.func.now())
    lastchange = Column(DateTime, server_default=sqlalchemy.sql.func.now())
    createdby = Column(ForeignKey("users.id"), index=True, nullable=True)
    changedby = Column(ForeignKey("users.id"), index=True, nullable=True)


class ProgramLanguageTypeModel(BaseModel):
    __tablename__ = "acprogramlanguages"
    id = UUIDColumn()
    name = Column(String)
    name_en = Column(String)
    # czech, english

    created = Column(DateTime, server_default=sqlalchemy.sql.func.now())
    lastchange = Column(DateTime, server_default=sqlalchemy.sql.func.now())
    createdby = Column(ForeignKey("users.id"), index=True, nullable=True)
    changedby = Column(ForeignKey("users.id"), index=True, nullable=True)

class ProgramLevelTypeModel(BaseModel):
    __tablename__ = "acprogramlevels"
    id = UUIDColumn()
    name = Column(String)
    name_en = Column(String)
    length = Column(Integer)
    priority = Column(Integer)  # 1 for Bc., 2 for Mgr. or NMgr., 3 for Ph.D.
    # bachelor, magister, doctoral

    created = Column(DateTime, server_default=sqlalchemy.sql.func.now())
    lastchange = Column(DateTime, server_default=sqlalchemy.sql.func.now())
    createdby = Column(ForeignKey("users.id"), index=True, nullable=True)
    changedby = Column(ForeignKey("users.id"), index=True, nullable=True)

class ProgramTitleTypeModel(BaseModel):
    __tablename__ = "acprogramtitles"
    id = UUIDColumn()
    name = Column(String)
    name_en = Column(String)
    # Bc., Mgr., Ing, ...

    created = Column(DateTime, server_default=sqlalchemy.sql.func.now())
    lastchange = Column(DateTime, server_default=sqlalchemy.sql.func.now())
    createdby = Column(ForeignKey("users.id"), index=True, nullable=True)
    changedby = Column(ForeignKey("users.id"), index=True, nullable=True)

class ProgramTypeModel(BaseModel):
    __tablename__ = "acprogramtypes"
    id = UUIDColumn()
    name = Column(String)
    name_en = Column(String)
    form_id = Column(ForeignKey("acprogramforms.id"), index=True)
    language_id = Column(ForeignKey("acprogramlanguages.id"), index=True)
    level_id = Column(ForeignKey("acprogramlevels.id"), index=True)
    title_id = Column(ForeignKey("acprogramtitles.id"), index=True)
    # combination

    created = Column(DateTime, server_default=sqlalchemy.sql.func.now())
    lastchange = Column(DateTime, server_default=sqlalchemy.sql.func.now())
    createdby = Column(ForeignKey("users.id"), index=True, nullable=True)
    changedby = Column(ForeignKey("users.id"), index=True, nullable=True)

class ProgramModel(BaseModel):
    __tablename__ = "acprograms"
    id = UUIDColumn()
    name = Column(String)
    name_en = Column(String)
    type_id = Column(ForeignKey("acprogramtypes.id"), index=True)

    created = Column(DateTime, server_default=sqlalchemy.sql.func.now())
    lastchange = Column(DateTime, server_default=sqlalchemy.sql.func.now())
    createdby = Column(ForeignKey("users.id"), index=True, nullable=True)
    changedby = Column(ForeignKey("users.id"), index=True, nullable=True)

class SubjectModel(BaseModel):
    """Aka Mathematics"""

    __tablename__ = "acsubjects"
    id = UUIDColumn()
    name = Column(String)
    name_en = Column(String)
    program_id = Column(ForeignKey("acprograms.id"), index=True)

    created = Column(DateTime, server_default=sqlalchemy.sql.func.now())
    lastchange = Column(DateTime, server_default=sqlalchemy.sql.func.now())
    createdby = Column(ForeignKey("users.id"), index=True, nullable=True)
    changedby = Column(ForeignKey("users.id"), index=True, nullable=True)

    # language_id = Column(ForeignKey('plan_subject_languages.id'))
    # program = relationship('StudyProgramModel', back_populates='subjects')
    # semesters = relationship('SemesterModel', back_populates='subject')
    # language = relationship('StudyLanguageModel', back_populates='subjects')


##############################################

# class StudyLanguageModel(BaseModel):
#     __tablename__ = "plan_subject_languages"
#     id = UUIDColumn()
#     name = Column(String)
#     last_change = Column(DateTime, server_default=sqlalchemy.sql.func.now())

#     #subjects = relationship('SubjectModel', back_populates='language')


#######################################


class SemesterModel(BaseModel):
    """Aka Mathematics, 2nd semester"""

    __tablename__ = "acsemesters"
    id = UUIDColumn()
    order = Column(Integer)
    credits = Column(Integer)
    subject_id = Column(ForeignKey("acsubjects.id"), index=True)
    classificationtype_id = Column(ForeignKey("acclassificationtypes.id"), index=True)

    created = Column(DateTime, server_default=sqlalchemy.sql.func.now())
    lastchange = Column(DateTime, server_default=sqlalchemy.sql.func.now())
    createdby = Column(ForeignKey("users.id"), index=True, nullable=True)
    changedby = Column(ForeignKey("users.id"), index=True, nullable=True)

    # subject = relationship('SubjectModel', back_populates='semesters')
    # classifications = relationship('ClassificationModel', back_populates='classificationsemesters')
    # themes = relationship('StudyThemesModel', back_populates='studysemesters')


##############################################
class ClassificationTypeModel(BaseModel):
    __tablename__ = "acclassificationtypes"
    id = UUIDColumn()
    name = Column(String)
    name_en = Column(String)
    # Z, KZ, Z+Zk, Zk, ...
    # classificationsemesters = relationship('SemesterModel', back_populates='classifications')

    created = Column(DateTime, server_default=sqlalchemy.sql.func.now())
    lastchange = Column(DateTime, server_default=sqlalchemy.sql.func.now())
    createdby = Column(ForeignKey("users.id"), index=True, nullable=True)
    changedby = Column(ForeignKey("users.id"), index=True, nullable=True)


##############################################
class TopicModel(BaseModel):
    """Aka Functions"""

    __tablename__ = "actopics"
    id = UUIDColumn()
    name = Column(String)
    name_en = Column(String)
    order = Column(Integer)

    semester_id = Column(ForeignKey("acsemesters.id"), index=True)

    created = Column(DateTime, server_default=sqlalchemy.sql.func.now())
    lastchange = Column(DateTime, server_default=sqlalchemy.sql.func.now())
    createdby = Column(ForeignKey("users.id"), index=True, nullable=True)
    changedby = Column(ForeignKey("users.id"), index=True, nullable=True)

    # studysemesters = relationship('SemesterModel', back_populates='themes')
    # items = relationship('StudyThemeItemModel', back_populates='theme')


##############################################


class LessonModel(BaseModel):
    """Lecture, 2h,"""

    __tablename__ = "aclessons"
    id = UUIDColumn()
    topic_id = Column(ForeignKey("actopics.id"), index=True)
    type_id = Column(ForeignKey("aclessontypes.id"), index=True)
    count = Column(Integer)

    created = Column(DateTime, server_default=sqlalchemy.sql.func.now())
    lastchange = Column(DateTime, server_default=sqlalchemy.sql.func.now())
    createdby = Column(ForeignKey("users.id"), index=True, nullable=True)
    changedby = Column(ForeignKey("users.id"), index=True, nullable=True)

    # type = relationship('ThemeTypeModel', back_populates='items')
    # theme = relationship('StudyThemeModel', back_populates='items')


class LessonTypeModel(BaseModel):
    __tablename__ = "aclessontypes"
    id = UUIDColumn()
    name = Column(String)
    name_en = Column(String)
    abbr = Column(String)

    created = Column(DateTime, server_default=sqlalchemy.sql.func.now())
    lastchange = Column(DateTime, server_default=sqlalchemy.sql.func.now())
    createdby = Column(ForeignKey("users.id"), index=True, nullable=True)
    changedby = Column(ForeignKey("users.id"), index=True, nullable=True)
    # lectures, excersise, laboratory, ...

    # items = relationship('StudyThemeItemModel', back_populates='type')


##############################################


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
            await conn.run_sync(BaseModel.metadata.create_all)
            print("BaseModel.metadata.create_all finished")

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
