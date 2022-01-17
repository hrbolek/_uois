import types
from sqlalchemy import Column, String, BigInteger, Integer, DateTime, ForeignKey, Sequence
from sqlalchemy.orm import relationship, backref
import datetime

from models.BaseModel import BaseModel
from models.GroupRelated.UserGroupModel import UserGroupModel
#from models.EventsRelated.EventUserModel import EventUserModel

class UserModel(BaseModel):
    __tablename__ = 'users'
    
    id = Column(BigInteger, Sequence('all_id_seq'), primary_key=True)
    name = Column(String)
    surname = Column(String)
    email = Column(String)
    
    lastchange = Column(DateTime, default=datetime.datetime.now)
    externalId = Column(BigInteger, index=True)

    groups = relationship('GroupModel', secondary=UserGroupModel, back_populates='users') #relationship(lazy='dynamic')
    #events = relationship('EventModel', secondary=EventUserModel, back_populates='users')
    roles = relationship('RoleModel', back_populates='user')