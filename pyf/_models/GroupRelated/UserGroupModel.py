import types
from sqlalchemy import Column, String, BigInteger, Integer, DateTime, ForeignKey, Sequence, Table
import datetime

from models.BaseModel import BaseModel
       
# class UserGroupModel(BaseModel):
#     __tablename__ = 'users_groups'
    
#     id = Column(BigInteger, Sequence('all_id_seq'), primary_key=True)
    
#     user_id = Column(BigInteger, ForeignKey('users.id'), primary_key=True)
#     group_id = Column(BigInteger, ForeignKey('groups.id'), primary_key=True)
#     lastchange = Column(DateTime, default=datetime.datetime.now)


UserGroupModel = Table('users_groups', BaseModel.metadata,
        Column('id', BigInteger, Sequence('all_id_seq'), primary_key=True),
        Column('user_id', ForeignKey('users.id'), primary_key=True),
        Column('group_id', ForeignKey('groups.id'), primary_key=True)

)
