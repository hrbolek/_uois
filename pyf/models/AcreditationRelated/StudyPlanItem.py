

import types
from sqlalchemy import Column, String, BigInteger, Integer, DateTime, ForeignKey, Sequence, Table
from sqlalchemy.orm import relationship
import datetime

from models.BaseModel import BaseModel
       
class StudyPlanItemModel(BaseModel):
    __tablename__ = 'studyplanitems'
    
    id = Column(BigInteger, Sequence('all_id_seq'), primary_key=True)
    name = Column(String)
    priority = Column(Integer)

    subjectSemesterTopic = Column(String)

    studyplan_id = Column(ForeignKey('studyplans.id'))
    studyplan = relationship('StudyPlanModel', back_populates='studyplanitems')

    #groups = relationship('StudyPlanItemGroupModel', back_populates='studyplanitem') #relationship(lazy='dynamic')
    events = relationship('StudyPlanItemEventModel', back_populates='studyplanitem')
    #teachers = relationship('StudyPlanItemTeacherModel', back_populates='studyplanitem')


class StudyPlanItemEventModel(BaseModel):
    __tablename__ = 'studyplanitemevents'
    id = Column(BigInteger, Sequence('all_id_seq'), primary_key=True)
    studyplanitem_id = Column(ForeignKey('studyplanitems.id'))
    event_id = Column(ForeignKey('events.id'))

    studyplanitem = relationship('StudyPlanItemModel', back_populates='events')

# class StudyPlanItemTeacherModel(BaseModel):
#     __tablename__ = 'studyplanitemteachers'
    
#     id = Column(BigInteger, Sequence('all_id_seq'), primary_key=True)

#     teacher_id = Column(ForeignKey('users.id'))
#     #teacher = relationship('UserModel')

#     studyplanitem_id = Column(ForeignKey('studyplanitems.id'))
#     #studyplanitem = relationship('StudyPlanItemModel', back_populates='teachers')

# class StudyPlanItemGroupModel(BaseModel):
#     __tablename__ = 'studyplanitemgroups'
    
#     id = Column(BigInteger, Sequence('all_id_seq'), primary_key=True)

#     group_id = Column(ForeignKey('groups.id'))
#     #group = relationship('GroupModel')

#     studyplanitem_id = Column(ForeignKey('studyplanitems.id'))
#     #studyplanitem = relationship('StudyPlanItemModel', back_populates='groups')

