import types
from sqlalchemy import Column, String, BigInteger, Integer, DateTime, ForeignKey, Sequence
from sqlalchemy.orm import relationship, backref
import datetime

from models.BaseModel import BaseModel

class SubjectSemesterModel(BaseModel):
    __tablename__ = 'subjectsemesters'

    id = Column(BigInteger, Sequence('all_id_seq'), primary_key=True)
    name = Column(String)
    
    lastchange = Column(DateTime, default=datetime.datetime.now)

    subject_id = Column(ForeignKey('subjects.id'))
    subject = relationship('SubjectModel', back_populates='subjectsemesters')

    topics = relationship('SubjectTopicModel', back_populates='subjectsemester')