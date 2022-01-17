import types
from sqlalchemy import Column, String, BigInteger, Integer, DateTime, ForeignKey, Sequence, Table
import datetime

from models.BaseModel import BaseModel
       
class AcreaditationUserRoleTypeModel(BaseModel):
    __tablename__ = 'acreditationuserroletypes'
    
    id = Column(BigInteger, Sequence('all_id_seq'), primary_key=True)
    name = Column(String)

class ProgramUserRoleModel(BaseModel):
    __tablename__ = 'programuserroles'
    
    id = Column(BigInteger, Sequence('all_id_seq'), primary_key=True)
    name = Column(String)
    role_id = Column(ForeignKey('acreditationuserroletypes.id'))
    user_id = Column(ForeignKey('users.id')) 
    program_id = Column(ForeignKey('programs.id')) 

class SubjectUserRoleModel(BaseModel):
    __tablename__ = 'subjectuserroles'
    
    id = Column(BigInteger, Sequence('all_id_seq'), primary_key=True)
    name = Column(String)
    role_id = Column(ForeignKey('acreditationuserroletypes.id'))
    user_id = Column(ForeignKey('users.id')) 
    subject_id = Column(ForeignKey('subjects.id')) 

class StudyPlanUserRoleModel(BaseModel):
    __tablename__ = 'studyplanuserroles'
    
    id = Column(BigInteger, Sequence('all_id_seq'), primary_key=True)
    name = Column(String)
    role_id = Column(ForeignKey('acreditationuserroletypes.id'))
    user_id = Column(ForeignKey('users.id')) 
    studyplan_id = Column(ForeignKey('studyplans.id')) 