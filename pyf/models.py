from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, String, BigInteger, DateTime, TIMESTAMP
from sqlalchemy import Table, ForeignKey, Sequence, text
from sqlalchemy.sql import func

import datetime


from sqlalchemy.sql.sqltypes import TIMESTAMP

def getBaseModel():
    """creates and cache a BaseModel
    
    Returns
    -------
    BaseModel
        it is instance of declarative_base from SQLAlchemy
    """
    BaseModel = declarative_base()
    print('BaseModel cached')
    return BaseModel


BaseModel = getBaseModel()


all_id_sequence = Sequence('all_id_seq', metadata=BaseModel.metadata)

# https://docs.sqlalchemy.org/en/14/core/defaults.html#triggered-columns
def idColumn():
    #return Column(BigInteger, all_id_sequence, server_default=all_id_sequence.next_value(), primary_key=True, unique=True)
    #https://www.postgresql.org/docs/13/functions-uuid.html
    #SELECT gen_random_uuid () as uuid;
    return Column(String, server_default=text("gen_random_uuid()"), primary_key=True, unique=True)

#createdColumn = Column(DateTime, server_default=func.sysdate())

# https://docs.sqlalchemy.org/en/14/dialects/mysql.html#mysql-timestamp-onupdate
#updated = Column(TIMESTAMP, server_default=text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"))
def lastchangeColumn():
    return Column(DateTime, server_default=func.now())

#-----------------------------------------------------------------------
# User
#-----------------------------------------------------------------------

class UserModel(BaseModel):
    __tablename__ = 'users'
    
    id = idColumn() #Column(BigInteger, Sequence('all_id_seq'), primary_key=True)
    name = Column(String)
    surname = Column(String)
    email = Column(String)
    
    lastchange = lastchangeColumn()#Column(DateTime, default=datetime.datetime.now)
    externalId = Column(BigInteger, index=True)
    UCO = Column(String, index=True)
    VaVId = Column(String, index=True)


#-----------------------------------------------------------------------
# Group related
#-----------------------------------------------------------------------

# UserGroupModel = Table('users_groups', BaseModel.metadata,
#         Column('id', BigInteger, all_id_sequence, server_default=all_id_sequence.next_value(), primary_key=True),
#         Column('user_id', ForeignKey('users.id'), primary_key=True),
#         Column('group_id', ForeignKey('groups.id'), primary_key=True)

# )

class UserGroupModel(BaseModel):
    __tablename__ = 'users_groups'
    id = idColumn()
    user_id = Column(ForeignKey('users.id'), index=True)
    group_id = Column(ForeignKey('groups.id'), index=True)

class GroupModel(BaseModel):
    __tablename__ = 'groups'
    
    id = idColumn()
    name = Column(String)
    abbreviation = Column(String)
    lastchange = lastchangeColumn()#Column(DateTime, default=datetime.datetime.now)
    entryYearId = Column(BigInteger)
    externalId = Column(String, index=True)
    UIC = Column(String, index=True)

    grouptype_id = Column(ForeignKey('grouptypes.id'), index=True)

class GroupConnectionModel(BaseModel):
    __tablename__ = 'groups_groups'
    
    id = idColumn()
    child_id = Column(ForeignKey('groups.id'), index=True)
    parent_id = Column(ForeignKey('groups.id'), index=True)

class GroupTypeModel(BaseModel):
    __tablename__ = 'grouptypes'
    
    id = idColumn()
    name = Column(String)

#-----------------------------------------------------------------------
# Roles of an User in a Group
#-----------------------------------------------------------------------

class RoleModel(BaseModel):
    __tablename__ = 'roles'

    id = idColumn()#Column(BigInteger, Sequence('all_id_seq'), primary_key=True)
    name = Column(String)
    lastchange = lastchangeColumn()#Column(DateTime, default=datetime.datetime.now)

    roletype_id = Column(ForeignKey('grouproletypes.id'), index=True)
    user_id = Column(ForeignKey('users.id'), index=True)
    group_id = Column(ForeignKey('groups.id'), index=True)

class RoleTypeModel(BaseModel):
    __tablename__ = 'grouproletypes'

    id = idColumn()#Column(BigInteger, Sequence('all_id_seq'), primary_key=True)
    name = Column(String)

#-----------------------------------------------------------------------
# Facility related
#-----------------------------------------------------------------------

class ArealModel(BaseModel):
    __tablename__ = 'areals'

    id = idColumn()#Column(BigInteger, Sequence('all_id_seq'), primary_key=True)
    name = Column(String)
    externalId = Column(String, index=True)
    lastchange = lastchangeColumn()#Column(DateTime, default=datetime.datetime.now)

class BuildingModel(BaseModel):
    __tablename__ = 'buildings'

    id = idColumn()#Column(BigInteger, Sequence('all_id_seq'), primary_key=True)
    name = Column(String)
    lastchange = lastchangeColumn()#Column(DateTime, default=datetime.datetime.now)
    externalId = Column(String, index=True)

    areal_id = Column(ForeignKey('areals.id'), index=True)

class RoomModel(BaseModel):
    __tablename__ = 'rooms'

    id = idColumn()#Column(BigInteger, Sequence('all_id_seq'), primary_key=True)
    name = Column(String)
    lastchange = lastchangeColumn()#Column(DateTime, default=datetime.datetime.now)
    externalId = Column(String, index=True)

    building_id = Column(ForeignKey('buildings.id'), index=True)

#-----------------------------------------------------------------------
# Event related
#-----------------------------------------------------------------------

class EventModel(BaseModel):
    __tablename__ = 'events'
    
    id = idColumn()#Column(BigInteger, Sequence('all_id_seq'), primary_key=True)
    start = Column(DateTime)
    end = Column(DateTime)
    label = Column(String)
    externalId = Column(String, index=True)
    lastchange = lastchangeColumn()#Column(DateTime, default=datetime.datetime.now)

class EventUserModel(BaseModel):
    __tablename__ = 'events_users'

    id = idColumn()#Column(BigInteger, Sequence('all_id_seq'), primary_key=True)
    user_id = Column(ForeignKey('users.id'), index=True)
    event_id = Column(ForeignKey('events.id'), index=True)

class EventGroupModel(BaseModel):
    __tablename__ = 'events_groups'

    id = idColumn()#Column(BigInteger, Sequence('all_id_seq'), primary_key=True)
    group_id = Column(ForeignKey('groups.id'), index=True)
    event_id = Column(ForeignKey('events.id'), index=True)

class EventRoomModel(BaseModel):
    __tablename__ = 'events_rooms'

    id = idColumn()#Column(BigInteger, Sequence('all_id_seq'), primary_key=True)
    room_id = Column(ForeignKey('rooms.id'), index=True)
    event_id = Column(ForeignKey('events.id'), index=True)

#-----------------------------------------------------------------------
# Acreditation related
#-----------------------------------------------------------------------
class AcreditationUserRoleTypeModel(BaseModel):
    __tablename__ = 'acreditationuserroletypes'
    id = idColumn()#Column(BigInteger, Sequence('all_id_seq'), primary_key=True)
    name = Column(String)

class ProgramModel(BaseModel):
    __tablename__ = 'programs'
    
    id = idColumn()#Column(BigInteger, Sequence('all_id_seq'), primary_key=True)
    name = Column(String)
    
    lastchange = lastchangeColumn()#Column(DateTime, default=datetime.datetime.now)
    externalId = Column(BigInteger, index=True)

class ProgramUserModel(BaseModel):
    __tablename__ = 'programs_users'

    id = idColumn()#Column(BigInteger, Sequence('all_id_seq'), primary_key=True)
    program_id = Column(ForeignKey('programs.id'), index=True)
    user_id = Column(ForeignKey('users.id'), index=True)
    roletype_id =  Column(ForeignKey('acreditationuserroletypes.id'), index=True)

class SubjectModel(BaseModel):
    __tablename__ = 'subjects'
    
    id = idColumn()#Column(BigInteger, Sequence('all_id_seq'), primary_key=True)
    name = Column(String)
    
    lastchange = lastchangeColumn()#Column(DateTime, default=datetime.datetime.now)
    externalId = Column(String, index=True)

    program_id = Column(ForeignKey('programs.id'), index=True)

class SubjectUserModel(BaseModel):
    __tablename__ = 'subjects_users'
    
    id = idColumn()#Column(BigInteger, Sequence('all_id_seq'), primary_key=True)
    subject_id = Column(ForeignKey('subjects.id'), index=True)
    user_id = Column(ForeignKey('users.id'), index=True)
    roletype_id =  Column(ForeignKey('acreditationuserroletypes.id'), index=True)

class SubjectSemesterModel(BaseModel):
    __tablename__ = 'subjectsemesters'

    id = idColumn()#Column(BigInteger, Sequence('all_id_seq'), primary_key=True)
    name = Column(String)
    
    lastchange = lastchangeColumn()#Column(DateTime, default=datetime.datetime.now)

    subject_id = Column(ForeignKey('subjects.id'), index=True)

class SubjectTopicModel(BaseModel):
    __tablename__ = 'subjecttopics'
    
    id = idColumn()#Column(BigInteger, Sequence('all_id_seq'), primary_key=True)
    name = Column(String)
    externalId = Column(String, index=True)

    subjectsemester_id = Column(ForeignKey('subjectsemesters.id'), index=True)

class SubjectTopicUserModel(BaseModel):
    __tablename__ = 'subjecttopics_users'
    
    id = idColumn()#Column(BigInteger, Sequence('all_id_seq'), primary_key=True)
    subjecttopic_id = Column(ForeignKey('subjecttopics.id'), index=True)
    user_id = Column(ForeignKey('users.id'), index=True)
    roletype_id =  Column(ForeignKey('acreditationuserroletypes.id'), index=True)

#-----------------------------------------------------------------------
# Study Plan (PSP) related
#-----------------------------------------------------------------------

class StudyPlanModel(BaseModel):
    __tablename__ = 'studyplans'
    
    id = idColumn()#Column(BigInteger, Sequence('all_id_seq'), primary_key=True)
    name = Column(String)
    externalId = Column(String, index=True)

class StudyPlanGroupsModel(BaseModel):
    __tablename__ = 'studyplans_groups'
    
    id = idColumn()#Column(BigInteger, Sequence('all_id_seq'), primary_key=True)
    
    studyplan_id = Column(ForeignKey('studyplans.id'), index=True)
    group_id = Column(ForeignKey('groups.id'), index=True)

class StudyPlanItemModel(BaseModel):
    __tablename__ = 'studyplanitems'
    
    id = idColumn()#Column(BigInteger, Sequence('all_id_seq'), primary_key=True)
    name = Column(String)
    priority = Column(BigInteger)

    subjectSemesterTopic = Column(String)
    externalId = Column(String, index=True)

    studyplan_id = Column(ForeignKey('studyplans.id'), index=True)

class StudyPlanItemEventModel(BaseModel):
    __tablename__ = 'studyplanitem_events'
    id = idColumn()#Column(BigInteger, Sequence('all_id_seq'), primary_key=True)

    studyplanitem_id = Column(ForeignKey('studyplanitems.id'), index=True)
    event_id = Column(ForeignKey('events.id'), index=True)

class StudyPlanItemTeacherModel(BaseModel):
    __tablename__ = 'studyplanitem_teachers'
    
    id = idColumn()#Column(BigInteger, Sequence('all_id_seq'), primary_key=True)

    teacher_id = Column(ForeignKey('users.id'), index=True)
    studyplanitem_id = Column(ForeignKey('studyplanitems.id'), index=True)

class StudyPlanItemGroupModel(BaseModel):
    __tablename__ = 'studyplanitem_groups'
    
    id = idColumn()#Column(BigInteger, Sequence('all_id_seq'), primary_key=True)

    group_id = Column(ForeignKey('groups.id'), index=True)
    studyplanitem_id = Column(ForeignKey('studyplanitems.id'), index=True)

