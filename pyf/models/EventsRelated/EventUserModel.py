import types
from sqlalchemy import Column, String, BigInteger, Integer, DateTime, ForeignKey, Sequence, Table
import datetime

from models.BaseModel import BaseModel
       
EventUserModel = Table('events_users', BaseModel.metadata,
        Column('id', BigInteger, Sequence('all_id_seq'), primary_key=True),
        Column('users_id', ForeignKey('users.id'), primary_key=True),
        Column('events_id', ForeignKey('events.id'), primary_key=True)

)