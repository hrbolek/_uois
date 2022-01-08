
from sqlalchemy import MetaData
from sqlalchemy.ext.automap import automap_base
from sqlalchemy import create_engine

from sqlalchemy import Column, String, BigInteger, DateTime, TIMESTAMP
from sqlalchemy import Table, ForeignKey, Sequence, text, relationship
from sqlalchemy.sql import func
    
class acreditationUserRoleTypeModel(BaseModel):
    __tablename__ = 'acreditationuserroletypes'
    __table_args__ = {'extend_existing': True} 
    
    programusermodel_collection = relationship('programUserModel')#(required=True)
    # programusermodel_collection = association_proxy('programusermodel_collection', 'keyword')
    
    subjectusermodel_collection = relationship('subjectUserModel')#(required=True)
    # subjectusermodel_collection = association_proxy('subjectusermodel_collection', 'keyword')
    
    subjecttopics_users_collection = relationship('subjecttopics_users')#(required=True)
    # subjecttopics_users_collection = association_proxy('subjecttopics_users_collection', 'keyword')
    
    

class arealModel(BaseModel):
    __tablename__ = 'areals'
    __table_args__ = {'extend_existing': True} 
    
    buildingmodel_collection = relationship('buildingModel')#(required=True)
    # buildingmodel_collection = association_proxy('buildingmodel_collection', 'keyword')
    
    

class buildingModel(BaseModel):
    __tablename__ = 'buildings'
    __table_args__ = {'extend_existing': True} 
    
    arealmodel = relationship('arealModel')#(required=True)
    # arealmodel = association_proxy('arealmodel', 'keyword')
    
    roommodel_collection = relationship('roomModel')#(required=True)
    # roommodel_collection = association_proxy('roommodel_collection', 'keyword')
    
    

class eventGroupModel(BaseModel):
    __tablename__ = 'events_groups'
    __table_args__ = {'extend_existing': True} 
    
    events = relationship('events')#(required=True)
    # events = association_proxy('events', 'keyword')
    
    groupmodel = relationship('groupModel')#(required=True)
    # groupmodel = association_proxy('groupmodel', 'keyword')
    
    

class eventRoomModel(BaseModel):
    __tablename__ = 'events_rooms'
    __table_args__ = {'extend_existing': True} 
    
    events = relationship('events')#(required=True)
    # events = association_proxy('events', 'keyword')
    
    roommodel = relationship('roomModel')#(required=True)
    # roommodel = association_proxy('roommodel', 'keyword')
    
    

class eventUserModel(BaseModel):
    __tablename__ = 'events_users'
    __table_args__ = {'extend_existing': True} 
    
    events = relationship('events')#(required=True)
    # events = association_proxy('events', 'keyword')
    
    usermodel = relationship('userModel')#(required=True)
    # usermodel = association_proxy('usermodel', 'keyword')
    
    

class events(BaseModel):
    __tablename__ = 'events'
    __table_args__ = {'extend_existing': True} 
    
    eventusermodel_collection = relationship('eventUserModel')#(required=True)
    # eventusermodel_collection = association_proxy('eventusermodel_collection', 'keyword')
    
    eventgroupmodel_collection = relationship('eventGroupModel')#(required=True)
    # eventgroupmodel_collection = association_proxy('eventgroupmodel_collection', 'keyword')
    
    studyplanitem_events_collection = relationship('studyplanitem_events')#(required=True)
    # studyplanitem_events_collection = association_proxy('studyplanitem_events_collection', 'keyword')
    
    eventroommodel_collection = relationship('eventRoomModel')#(required=True)
    # eventroommodel_collection = association_proxy('eventroommodel_collection', 'keyword')
    
    

class groupGroupModel(BaseModel):
    __tablename__ = 'groups_groups'
    __table_args__ = {'extend_existing': True} 
    
    groupmodel = relationship('groupModel')#(required=True)
    # groupmodel = association_proxy('groupmodel', 'keyword')
    
    

class groupModel(BaseModel):
    __tablename__ = 'groups'
    __table_args__ = {'extend_existing': True} 
    
    grouptypemodel = relationship('groupTypeModel')#(required=True)
    # grouptypemodel = association_proxy('grouptypemodel', 'keyword')
    
    groupgroupmodel_collection = relationship('groupGroupModel')#(required=True)
    # groupgroupmodel_collection = association_proxy('groupgroupmodel_collection', 'keyword')
    
    usergroupmodel_collection = relationship('userGroupModel')#(required=True)
    # usergroupmodel_collection = association_proxy('usergroupmodel_collection', 'keyword')
    
    rolemodel_collection = relationship('roleModel')#(required=True)
    # rolemodel_collection = association_proxy('rolemodel_collection', 'keyword')
    
    eventgroupmodel_collection = relationship('eventGroupModel')#(required=True)
    # eventgroupmodel_collection = association_proxy('eventgroupmodel_collection', 'keyword')
    
    studyplansgroupmodel_collection = relationship('studyPlansGroupModel')#(required=True)
    # studyplansgroupmodel_collection = association_proxy('studyplansgroupmodel_collection', 'keyword')
    
    studyplanitem_groups_collection = relationship('studyplanitem_groups')#(required=True)
    # studyplanitem_groups_collection = association_proxy('studyplanitem_groups_collection', 'keyword')
    
    

class groupRoleTypeModel(BaseModel):
    __tablename__ = 'grouproletypes'
    __table_args__ = {'extend_existing': True} 
    
    rolemodel_collection = relationship('roleModel')#(required=True)
    # rolemodel_collection = association_proxy('rolemodel_collection', 'keyword')
    
    

class groupTypeModel(BaseModel):
    __tablename__ = 'grouptypes'
    __table_args__ = {'extend_existing': True} 
    
    groupmodel_collection = relationship('groupModel')#(required=True)
    # groupmodel_collection = association_proxy('groupmodel_collection', 'keyword')
    
    

class programModel(BaseModel):
    __tablename__ = 'programs'
    __table_args__ = {'extend_existing': True} 
    
    programusermodel_collection = relationship('programUserModel')#(required=True)
    # programusermodel_collection = association_proxy('programusermodel_collection', 'keyword')
    
    subjectmodel_collection = relationship('subjectModel')#(required=True)
    # subjectmodel_collection = association_proxy('subjectmodel_collection', 'keyword')
    
    

class programUserModel(BaseModel):
    __tablename__ = 'programs_users'
    __table_args__ = {'extend_existing': True} 
    
    usermodel = relationship('userModel')#(required=True)
    # usermodel = association_proxy('usermodel', 'keyword')
    
    acreditationuserroletypemodel = relationship('acreditationUserRoleTypeModel')#(required=True)
    # acreditationuserroletypemodel = association_proxy('acreditationuserroletypemodel', 'keyword')
    
    programmodel = relationship('programModel')#(required=True)
    # programmodel = association_proxy('programmodel', 'keyword')
    
    

class roleModel(BaseModel):
    __tablename__ = 'roles'
    __table_args__ = {'extend_existing': True} 
    
    grouproletypemodel = relationship('groupRoleTypeModel')#(required=True)
    # grouproletypemodel = association_proxy('grouproletypemodel', 'keyword')
    
    groupmodel = relationship('groupModel')#(required=True)
    # groupmodel = association_proxy('groupmodel', 'keyword')
    
    usermodel = relationship('userModel')#(required=True)
    # usermodel = association_proxy('usermodel', 'keyword')
    
    

class roomModel(BaseModel):
    __tablename__ = 'rooms'
    __table_args__ = {'extend_existing': True} 
    
    buildingmodel = relationship('buildingModel')#(required=True)
    # buildingmodel = association_proxy('buildingmodel', 'keyword')
    
    eventroommodel_collection = relationship('eventRoomModel')#(required=True)
    # eventroommodel_collection = association_proxy('eventroommodel_collection', 'keyword')
    
    

class studyPlanItemModel(BaseModel):
    __tablename__ = 'studyplanitems'
    __table_args__ = {'extend_existing': True} 
    
    studyplanmodel = relationship('studyPlanModel')#(required=True)
    # studyplanmodel = association_proxy('studyplanmodel', 'keyword')
    
    studyplanitem_events_collection = relationship('studyplanitem_events')#(required=True)
    # studyplanitem_events_collection = association_proxy('studyplanitem_events_collection', 'keyword')
    
    studyplanitem_teachers_collection = relationship('studyplanitem_teachers')#(required=True)
    # studyplanitem_teachers_collection = association_proxy('studyplanitem_teachers_collection', 'keyword')
    
    studyplanitem_groups_collection = relationship('studyplanitem_groups')#(required=True)
    # studyplanitem_groups_collection = association_proxy('studyplanitem_groups_collection', 'keyword')
    
    

class studyPlanModel(BaseModel):
    __tablename__ = 'studyplans'
    __table_args__ = {'extend_existing': True} 
    
    studyplanitemmodel_collection = relationship('studyPlanItemModel')#(required=True)
    # studyplanitemmodel_collection = association_proxy('studyplanitemmodel_collection', 'keyword')
    
    studyplansgroupmodel_collection = relationship('studyPlansGroupModel')#(required=True)
    # studyplansgroupmodel_collection = association_proxy('studyplansgroupmodel_collection', 'keyword')
    
    

class studyPlansGroupModel(BaseModel):
    __tablename__ = 'studyplans_groups'
    __table_args__ = {'extend_existing': True} 
    
    studyplanmodel = relationship('studyPlanModel')#(required=True)
    # studyplanmodel = association_proxy('studyplanmodel', 'keyword')
    
    groupmodel = relationship('groupModel')#(required=True)
    # groupmodel = association_proxy('groupmodel', 'keyword')
    
    

class studyplanitem_events(BaseModel):
    __tablename__ = 'studyplanitem_events'
    __table_args__ = {'extend_existing': True} 
    
    studyplanitemmodel = relationship('studyPlanItemModel')#(required=True)
    # studyplanitemmodel = association_proxy('studyplanitemmodel', 'keyword')
    
    events = relationship('events')#(required=True)
    # events = association_proxy('events', 'keyword')
    
    

class studyplanitem_groups(BaseModel):
    __tablename__ = 'studyplanitem_groups'
    __table_args__ = {'extend_existing': True} 
    
    studyplanitemmodel = relationship('studyPlanItemModel')#(required=True)
    # studyplanitemmodel = association_proxy('studyplanitemmodel', 'keyword')
    
    groupmodel = relationship('groupModel')#(required=True)
    # groupmodel = association_proxy('groupmodel', 'keyword')
    
    

class studyplanitem_teachers(BaseModel):
    __tablename__ = 'studyplanitem_teachers'
    __table_args__ = {'extend_existing': True} 
    
    usermodel = relationship('userModel')#(required=True)
    # usermodel = association_proxy('usermodel', 'keyword')
    
    studyplanitemmodel = relationship('studyPlanItemModel')#(required=True)
    # studyplanitemmodel = association_proxy('studyplanitemmodel', 'keyword')
    
    

class subjectModel(BaseModel):
    __tablename__ = 'subjects'
    __table_args__ = {'extend_existing': True} 
    
    programmodel = relationship('programModel')#(required=True)
    # programmodel = association_proxy('programmodel', 'keyword')
    
    subjectusermodel_collection = relationship('subjectUserModel')#(required=True)
    # subjectusermodel_collection = association_proxy('subjectusermodel_collection', 'keyword')
    
    subjectsemestermodel_collection = relationship('subjectSemesterModel')#(required=True)
    # subjectsemestermodel_collection = association_proxy('subjectsemestermodel_collection', 'keyword')
    
    

class subjectSemesterModel(BaseModel):
    __tablename__ = 'subjectsemesters'
    __table_args__ = {'extend_existing': True} 
    
    subjectmodel = relationship('subjectModel')#(required=True)
    # subjectmodel = association_proxy('subjectmodel', 'keyword')
    
    subjecttopicmodel_collection = relationship('subjectTopicModel')#(required=True)
    # subjecttopicmodel_collection = association_proxy('subjecttopicmodel_collection', 'keyword')
    
    

class subjectTopicModel(BaseModel):
    __tablename__ = 'subjecttopics'
    __table_args__ = {'extend_existing': True} 
    
    subjectsemestermodel = relationship('subjectSemesterModel')#(required=True)
    # subjectsemestermodel = association_proxy('subjectsemestermodel', 'keyword')
    
    subjecttopics_users_collection = relationship('subjecttopics_users')#(required=True)
    # subjecttopics_users_collection = association_proxy('subjecttopics_users_collection', 'keyword')
    
    

class subjectUserModel(BaseModel):
    __tablename__ = 'subjects_users'
    __table_args__ = {'extend_existing': True} 
    
    acreditationuserroletypemodel = relationship('acreditationUserRoleTypeModel')#(required=True)
    # acreditationuserroletypemodel = association_proxy('acreditationuserroletypemodel', 'keyword')
    
    usermodel = relationship('userModel')#(required=True)
    # usermodel = association_proxy('usermodel', 'keyword')
    
    subjectmodel = relationship('subjectModel')#(required=True)
    # subjectmodel = association_proxy('subjectmodel', 'keyword')
    
    

class subjecttopics_users(BaseModel):
    __tablename__ = 'subjecttopics_users'
    __table_args__ = {'extend_existing': True} 
    
    usermodel = relationship('userModel')#(required=True)
    # usermodel = association_proxy('usermodel', 'keyword')
    
    acreditationuserroletypemodel = relationship('acreditationUserRoleTypeModel')#(required=True)
    # acreditationuserroletypemodel = association_proxy('acreditationuserroletypemodel', 'keyword')
    
    subjecttopicmodel = relationship('subjectTopicModel')#(required=True)
    # subjecttopicmodel = association_proxy('subjecttopicmodel', 'keyword')
    
    

class userGroupModel(BaseModel):
    __tablename__ = 'users_groups'
    __table_args__ = {'extend_existing': True} 
    
    groupmodel = relationship('groupModel')#(required=True)
    # groupmodel = association_proxy('groupmodel', 'keyword')
    
    usermodel = relationship('userModel')#(required=True)
    # usermodel = association_proxy('usermodel', 'keyword')
    
    

class userModel(BaseModel):
    __tablename__ = 'users'
    __table_args__ = {'extend_existing': True} 
    
    eventusermodel_collection = relationship('eventUserModel')#(required=True)
    # eventusermodel_collection = association_proxy('eventusermodel_collection', 'keyword')
    
    programusermodel_collection = relationship('programUserModel')#(required=True)
    # programusermodel_collection = association_proxy('programusermodel_collection', 'keyword')
    
    usergroupmodel_collection = relationship('userGroupModel')#(required=True)
    # usergroupmodel_collection = association_proxy('usergroupmodel_collection', 'keyword')
    
    rolemodel_collection = relationship('roleModel')#(required=True)
    # rolemodel_collection = association_proxy('rolemodel_collection', 'keyword')
    
    subjectusermodel_collection = relationship('subjectUserModel')#(required=True)
    # subjectusermodel_collection = association_proxy('subjectusermodel_collection', 'keyword')
    
    studyplanitem_teachers_collection = relationship('studyplanitem_teachers')#(required=True)
    # studyplanitem_teachers_collection = association_proxy('studyplanitem_teachers_collection', 'keyword')
    
    subjecttopics_users_collection = relationship('subjecttopics_users')#(required=True)
    # subjecttopics_users_collection = association_proxy('subjecttopics_users_collection', 'keyword')
    
    
