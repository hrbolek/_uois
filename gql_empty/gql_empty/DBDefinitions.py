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

class StudyProgramsModel(BaseModel):
    __tablename__ = "plan_study_programs"
    id = UUIDColumn()
    type = Column(String)
    lenght = Column(Integer)
    type_of_study = Column(String)
    name_id = Column(ForeignKey('name.id'))

    subjects = relationship('SubjectsOfStudyModel',back_populates='programs')
    names = relationship('ThemeNameModel', back_populates='nameprograms')

##############################################
class ThemeNameModel(BaseModel):
    __tablename__ = "plan_theme_name"
    id = UUIDColumn()
    name = Column(String)

    nameprograms = relationship('StudyProgramsModel',back_populates='names')
##############################################

class SubjectsOfStudyModel(BaseModel):
    __tablename__ = "plan_subjects_of_study"
    id = UUIDColumn()
    option_id = Column(ForeignKey('option.id'))
    subject_id = Column(ForeignKey('subject.id'))
    language_id = Column(ForeignKey('language.id'))

    programs = relationship('StudyProgramsModel', back_populates='subjects')
    semesters = relationship('SemestersOfStudyModel', back_populates='subsemesters')
    options = relationship('SubjectOptionModel', back_populates='optionsubjects')
    languages = relationship('StudyLanguageModel', back_populates='languagesubjects')

##############################################
class SubjectOptionModel(BaseModel):
    __tablename__= "plan_subject_option"
    id = UUIDColumn()
    name = Column(String)

    optionsubjects = relationship('SubjectsOfStudyModel',back_populates='options')

class StudyLanguageModel(BaseModel):
    __tablename__= "plan_study_language"
    id = UUIDColumn()
    name = Column(String)

    languagesubjects = relationship('SubjectsOfStudyModel', back_populates='languages')
#######################################

class SemestersOfStudyModel(BaseModel):
    __tablename__ = "plan_semesters_of_study"
    id = UUIDColumn()
    semester_number = Column(Integer)
    credits = Column(Integer)
    semester_id = Column(ForeignKey('semester.id'))
    classification_id = Column(ForeignKey('classification.id'))

    subsemesters = relationship('SubjectsOfStudyModel', back_populates='semesters')
    classifications = relationship('ClassificationModel', back_populates='classificationsemesters')
    themes = relationship('StudyThemesModel', back_populates='studysemesters')

##############################################
class ClassificationModel(BaseModel):
    __tablename__ = "plan_classification"
    id = UUIDColumn()
    name = Column(String)

    classificationsemesters = relationship('SemestersOfStudyModel',back_populates='classifications')
##############################################
class StudyThemesModel(BaseModel):
    __tablename__ = "plan_study_themes"
    id = UUIDColumn()
    unit = Column(Integer)
    theme_id = Column(ForeignKey('theme.id'))
    type_id = Column(ForeignKey('type.id'))

    studysemesters = relationship('SemestersOfStudyModel', back_populates='themes')
    types = relationship('ThemeTypeModel', back_populates='typethemes')

##############################################
class ThemeTypeModel(BaseModel):
    __tablename__= "plan_theme_type"
    id = UUIDColumn()
    name = Column(String)

    typethemes = relationship('StudyThemesModel', back_populates='types')
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
