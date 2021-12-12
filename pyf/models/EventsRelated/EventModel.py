import types
from sqlalchemy import Column, String, BigInteger, Integer, DateTime, ForeignKey, Sequence
import datetime
from sqlalchemy.orm import relationship, backref

from models.BaseModel import BaseModel
from models.EventsRelated.EventGroupModel import EventGroupModel
from models.EventsRelated.EventUserModel import EventUserModel

class EventModel(BaseModel):
    __tablename__ = 'events'
    
    id = Column(BigInteger, Sequence('all_id_seq'), primary_key=True)
    start = Column(DateTime)
    end = Column(DateTime)
    label = Column(String)
    externalId = Column(String, index=True)
    lastchange = Column(DateTime, default=datetime.datetime.now)

    users = relationship('UserModel', secondary=EventUserModel, back_populates='events') #relationship(lazy='dynamic')
    #groups = relationship('GroupModel', secondary=EventGroupModel, back_populates='events') #relationship(lazy='dynamic')
