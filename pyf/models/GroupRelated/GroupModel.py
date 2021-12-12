import types
from sqlalchemy import Column, String, BigInteger, Integer, DateTime, ForeignKey, Sequence
import datetime
from sqlalchemy.orm import relationship, backref

from ..BaseModel import BaseModel
from .UserGroupModel import UserGroupModel
#from .EventGroupModel import EventGroupModel
from .GroupTypeModel import GroupTypeModel

class GroupModel(BaseModel):
    __tablename__ = 'groups'
    
    id = Column(BigInteger, Sequence('all_id_seq'), primary_key=True)
    name = Column(String)
    
    lastchange = Column(DateTime, default=datetime.datetime.now)
    entryYearId = Column(Integer)

    externalId = Column(String, index=True)

    grouptype_id = Column(ForeignKey('grouptypes.id'))
    grouptype = relationship('GroupTypeModel', back_populates='groups')

    users = relationship('UserModel', secondary=UserGroupModel, back_populates='groups') #relationship(lazy='dynamic')

    roles = relationship('RoleModel', back_populates='group')
    #events = relationship('EventModel', secondary=EventGroupModel, back_populates='groups')