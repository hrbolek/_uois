import types
from sqlalchemy import Column, String, BigInteger, Integer, DateTime, ForeignKey, Sequence
import datetime
from sqlalchemy.orm import relationship, backref

from models.BaseModel import BaseModel
#from models.EventsRelated.EventGroupModel import EventGroupModel
#from models.EventsRelated.EventUserModel import EventUserModel
#from models.EventsRelated.EventRoomModel import EventRoomModel

class EventModel(BaseModel):
    __tablename__ = 'events'
    
    id = Column(BigInteger, Sequence('all_id_seq'), primary_key=True)
    start = Column(DateTime)
    end = Column(DateTime)
    label = Column(String)
    externalId = Column(String, index=True)
    lastchange = Column(DateTime, default=datetime.datetime.now)


    #userlinks = relationship('EventUserModel')
    #groupslinks = relationship('EventGroupModel')
    #roomlinks = relationship('EventRoomModel')
    #users = relationship('UserModel', secondary=EventUserModel)#, back_populates='events') #relationship(lazy='dynamic')
    
    #users = relationship('UserModel', 
    #    primaryjoin="EventModel.id==EventUserModel.event_id", 
    #    secondaryjoin="and_(EventUserModel.event_id==EventModel.id, EventUserModel.id==EventUserModel.id)")

    #users = relationship('EventUserModel') 
        #primaryjoin="events.id==events_users.event_id") 
        #secondaryjoin="and_(events_users.event_id==events.id, events_users.user_id==users.id)")

    #rooms = relationship('RoomModel', secondary=EventGroupModel)#, back_populates='events') #relationship(lazy='dynamic') 
    #groups = relationship('GroupModel', secondary=EventGroupModel, back_populates='events') #relationship(lazy='dynamic')
    #groups = relationship('GroupModel', secondary=EventGroupModel)#, back_populates='events') #relationship(lazy='dynamic')
