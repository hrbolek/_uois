import types
from sqlalchemy import Column, String, BigInteger, Integer, DateTime, ForeignKey, Sequence
from sqlalchemy.orm import relationship, backref
import datetime

from models.BaseModel import BaseModel

class SubjectTopicModel(BaseModel):
    __tablename__ = 'subjecttopics'
    
    id = Column(BigInteger, Sequence('all_id_seq'), primary_key=True)
    name = Column(String)

    subjectsemester_id = Column(ForeignKey('subjectsemesters.id'))
    subjectsemester = relationship('SubjectSemesterModel', back_populates='topics')