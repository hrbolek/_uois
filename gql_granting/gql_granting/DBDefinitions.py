import sqlalchemy
import datetime
from sqlalchemy import Column, String, BigInteger, Integer, DateTime, ForeignKey, Sequence, Table, Boolean
from sqlalchemy.dialects.postgresql import UUID

from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

BaseModel = declarative_base()


def UUIDColumn(name=None):
    if name is None:
        return Column(UUID(as_uuid=True), primary_key=True, server_default=sqlalchemy.text("gen_random_uuid()"),
                      unique=True)
    else:
        return Column(name, UUID(as_uuid=True), primary_key=True, server_default=sqlalchemy.text("gen_random_uuid()"),
                      unique=True)


# id = Column(UUID(as_uuid=True), primary_key=True, server_default=sqlalchemy.text("uuid_generate_v4()"),)

###########################################################################################################################
#
# zde definujte sve SQLAlchemy modely
# je-li treba, muzete definovat modely obsahujici jen id polozku, na ktere se budete odkazovat
#

class StudyProgramModel(BaseModel):
    __tablename__ = "plan_programs"
    id = UUIDColumn()
    type = Column(String)  # bachelor/master/doctor
    study_duration = Column(Integer)
    type_of_study = Column(String)  # milXciv
    name = Column(String)
    last_change = Column(DateTime, server_default=sqlalchemy.sql.func.now())
    # studiu kombinovane/dalkove
    subjects = relationship('SubjectModel', back_populates='program')


class SubjectModel(BaseModel):
    __tablename__ = "plan_subjects"
    id = UUIDColumn()
    name = Column(String)
    program_id = Column(ForeignKey('plan_programs.id'))
    language_id = Column(ForeignKey('plan_subject_languages.id'))
    last_change = Column(DateTime, server_default=sqlalchemy.sql.func.now())

    program = relationship('StudyProgramModel', back_populates='subjects')
    semesters = relationship('SemesterModel', back_populates='subject')
    language = relationship('StudyLanguageModel', back_populates='subjects')



##############################################

class StudyLanguageModel(BaseModel):
    __tablename__ = "plan_subject_languages"
    id = UUIDColumn()
    name = Column(String)
    last_change = Column(DateTime, server_default=sqlalchemy.sql.func.now())

    subjects = relationship('SubjectModel', back_populates='language')


#######################################

class SemesterModel(BaseModel):
    __tablename__ = "plan_semesters"
    id = UUIDColumn()
    semester_number = Column(Integer)
    credits = Column(Integer)
    subject_id = Column(ForeignKey('plan_subjects.id'))
    classification_id = Column(ForeignKey('plan_classifications.id'))
    last_change = Column(DateTime, server_default=sqlalchemy.sql.func.now())

    subject = relationship('SubjectModel', back_populates='semesters')
    classifications = relationship('ClassificationModel', back_populates='classificationsemesters')
    themes = relationship('StudyThemesModel', back_populates='studysemesters')


##############################################
class ClassificationModel(BaseModel):
    __tablename__ = "plan_classifications"
    id = UUIDColumn()
    name = Column(String)
    last_change = Column(DateTime, server_default=sqlalchemy.sql.func.now())

    classificationsemesters = relationship('SemesterModel', back_populates='classifications')


##############################################
class StudyThemeModel(BaseModel):
    __tablename__ = "plan_themes"
    id = UUIDColumn()
    name = Column(String)
    semester_id = Column(ForeignKey('plan_semesters.id'))
    last_change = Column(DateTime, server_default=sqlalchemy.sql.func.now())

    studysemesters = relationship('SemesterModel', back_populates='themes')
    items = relationship('StudyThemeItemModel', back_populates='theme')


##############################################

class StudyThemeItemModel(BaseModel):
    __tablename__ = "plan_items"
    id = UUIDColumn()
    theme_id = Column(ForeignKey('plan_themes.id'))
    type_id = Column(ForeignKey('plan_item_types.id'))
    lessons = Column(Integer)
    last_change = Column(DateTime, server_default=sqlalchemy.sql.func.now())

    type = relationship('ThemeTypeModel', back_populates='items')
    theme = relationship('StudyThemeModel', back_populates='items')


class ThemeTypeModel(BaseModel):
    __tablename__ = "plan_item_types"
    id = UUIDColumn()
    name = Column(String)
    last_change = Column(DateTime, server_default=sqlalchemy.sql.func.now())

    items = relationship('StudyThemeItemModel', back_populates='type')


##############################################


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
    database = os.environ.get("POSTGRES_DB", "data")
    hostWithPort = os.environ.get("POSTGRES_HOST", "postgres:5432")

    driver = "postgresql+asyncpg"  # "postgresql+psycopg2"
    connectionstring = f"{driver}://{user}:{password}@{hostWithPort}/{database}"

    return connectionstring
