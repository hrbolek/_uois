import types
from sqlalchemy import Column, String, BigInteger, Integer, DateTime, ForeignKey, Sequence
from sqlalchemy.orm import relationship, backref
import datetime

from models.BaseModel import BaseModel

class RoleModel(BaseModel):
    __tablename__ = 'roles'

    id = Column(BigInteger, Sequence('all_id_seq'), primary_key=True)
    name = Column(String)
    
    lastchange = Column(DateTime, default=datetime.datetime.now)

    roletype_id = Column(ForeignKey('roletypes.id'))
    roletype = relationship('RoleTypeModel', back_populates='roles')

    user_id = Column(ForeignKey('users.id'))
    user = relationship('UserModel', back_populates='roles')

    group_id = Column(ForeignKey('groups.id'))
    group = relationship('GroupModel', back_populates='roles')