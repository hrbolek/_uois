import types
from sqlalchemy import Column, String, BigInteger, Integer, DateTime, ForeignKey, Sequence
import datetime
from functools import cache

import sqlengine.sqlengine as SqlEngine

from . import BaseModel

@cache # funny thing, it makes from this function a singleton
def GetModels(BaseModel=BaseModel.getBaseModel(), unitedSequence=Sequence('all_id_seq')):
    """create elementary models for information systems

    Parameters
    ----------
    BaseModel
        represents the declarative_base instance from SQLAlchemy
    unitedSequence : Sequence
        represents a method for generating keys (usually ids) for database entities

    Returns
    -------
    (UserModel, GroupModel, RoleModel, GroupTypeModel, RoleTypeModel)
        tuple of models based on BaseModel, table names are hardcoded

    """

    #assert not(unitedSequence is None), "unitedSequence must be defined"
    print('Base models definition (UserModel, GroupModel, RoleModel, GroupTypeModel, RoleTypeModel)')
    class UserModel(BaseModel):
        __tablename__ = 'users'
        
        id = Column(BigInteger, unitedSequence, primary_key=True)
        name = Column(String)
        surname = Column(String)
        email = Column(String)
        
        lastchange = Column(DateTime, default=datetime.datetime.now)
        externalId = Column(BigInteger, index=True)


    class GroupModel(BaseModel):
        __tablename__ = 'groups'
        
        id = Column(BigInteger, unitedSequence, primary_key=True)
        name = Column(String)
        
        lastchange = Column(DateTime, default=datetime.datetime.now)
        entryYearId = Column(Integer)

        externalId = Column(String, index=True)
        
    class RoleModel(BaseModel):
        __tablename__ = 'roles'

        id = Column(BigInteger, unitedSequence, primary_key=True)
        name = Column(String)
        
        lastchange = Column(DateTime, default=datetime.datetime.now)

    class GroupTypeModel(BaseModel):
        __tablename__ = 'grouptypes'
        
        id = Column(BigInteger, unitedSequence, primary_key=True)
        name = Column(String)
        
    class RoleTypeModel(BaseModel):
        __tablename__ = 'roletypes'

        id = Column(BigInteger, unitedSequence, primary_key=True)
        name = Column(String)

    return UserModel, GroupModel, RoleModel, GroupTypeModel, RoleTypeModel


from . import Relations 
@cache
def BuildRelations():
    UserModel, GroupModel, RoleModel, GroupTypeModel, RoleTypeModel = GetModels()
    print('building relations between base models')

    Relations.defineRelationNM(UserModel, GroupModel)
    Relations.defineRelation1N(GroupTypeModel, GroupModel) 
    Relations.defineRelation1N(RoleTypeModel, RoleModel)
    Relations.defineRelation1N(GroupModel, RoleModel)
    Relations.defineRelation1N(UserModel, RoleModel)

    print('building relations between base models finished')
    #defineRelationNM(BaseModel, EventModel, UserModel, 'teachers', 'events')

    pass

from types import MappingProxyType

@cache
def ensureData(SessionMaker=None, session=None):
    def ensureDataItem(session, Model, name):
        itemRecords = session.query(Model).filter(Model.name == name).all()
        itemRecordsLen = len(itemRecords)
        if itemRecordsLen == 0:
            itemRecord = Model(name=name)
            session.add(itemRecord)
            session.commit()
        else:
            assert itemRecordsLen == 1, f'Database has inconsistencies {Model}, {name}'
            itemRecord = itemRecords[0]
        return itemRecord.id

    UserModel, GroupModel, RoleModel, GroupTypeModel, RoleTypeModel = GetModels()
    session = SessionMaker() if session is None else session
    try:
        departmentTypeId = ensureDataItem(session, GroupTypeModel, 'department')
        facultyTypeId = ensureDataItem(session, GroupTypeModel, 'faculty')
        studyGroupId =  ensureDataItem(session, GroupTypeModel, 'studygroup')

        departmentHeadRoleTypeId = ensureDataItem(session, RoleTypeModel, 'head of department')
        deanRoleTypeId = ensureDataItem(session, RoleTypeModel, 'dean')
        viceDeanRoleTypeId = ensureDataItem(session, RoleTypeModel, 'vice dean')
        rectorRoleTypeId = ensureDataItem(session, RoleTypeModel, 'rector')
        viceRectorRoleTypeId = ensureDataItem(session, RoleTypeModel, 'vice rector')

        result = {
            'departmentTypeId': departmentTypeId,
            'facultyTypeId': facultyTypeId,
            'studyGroupId': studyGroupId,
            'departmentHeadRoleTypeId': departmentHeadRoleTypeId,
            'deanRoleTypeId': deanRoleTypeId,
            'viceDeanRoleTypeId': viceDeanRoleTypeId,
            'rectorRoleTypeId': rectorRoleTypeId,
            'viceRectorRoleTypeId': viceRectorRoleTypeId
        }    
    finally:
        session.close()
    return MappingProxyType(result)


import random
def randomUser(mod='main'):
    surNames = [
        'Novák', 'Nováková', 'Svobodová', 'Svoboda', 'Novotná',
        'Novotný', 'Dvořáková', 'Dvořák', 'Černá', 'Černý', 
        'Procházková', 'Procházka', 'Kučerová', 'Kučera', 'Veselá',
        'Veselý', 'Horáková', 'Krejčí', 'Horák', 'Němcová', 
        'Marková', 'Němec', 'Pokorná', 'Pospíšilová','Marek'
    ]

    names = [
        'Jiří', 'Jan', 'Petr', 'Jana', 'Marie', 'Josef',
        'Pavel', 'Martin', 'Tomáš', 'Jaroslav', 'Eva',
        'Miroslav', 'Hana', 'Anna', 'Zdeněk', 'Václav',
        'Michal', 'František', 'Lenka', 'Kateřina',
        'Lucie', 'Jakub', 'Milan', 'Věra', 'Alena'
    ]

    name1 = random.choice(names)
    name2 = random.choice(names)
    name3 = random.choice(surNames)
    email = f'{name1}.{name2}.{name3}@{mod}.university.world'
    return {'name': f'{name1} {name2}', 'surname': name3, 'email': email}

def PopulateRandomData(SessionMaker=None, session=None):
    session = SessionMaker() if session is None else session
    try:
        UserModel, GroupModel, RoleModel, GroupTypeModel, RoleTypeModel = GetModels()
        
        typeIds = ensureData(SessionMaker)
        
        allTeachersGroup = GroupModel(name='teachers')
        allStudentsGroup = GroupModel(name='students')

        session.add(allTeachersGroup)
        session.add(allStudentsGroup)
        session.commit()
        
        def RandomizedStudents(faculty, studyGroup, count=10):
            for _ in range(count):
                student = randomUser(mod=faculty.name)
                studentRecord = UserModel(**student)
                session.add(studentRecord)
                faculty.users.append(studentRecord)
                studyGroup.users.append(studentRecord)
                allStudentsGroup.users.append(studentRecord)
            session.commit()
        
        def RandomizedStudyGroup(faculty):
            strs = ['KB', 'BSV', 'ASV', 'ZM', 'IT', 'EL', 'ST', 'GEO', 'MET']
            appendixes = ['', '-K', '-C', '-O', '-V', '-X']
            name = f"{faculty.name}5-{random.choice([1, 2, 3, 4, 5])}{random.choice(strs)}{random.choice(appendixes)}"
            studyGroupRecord = GroupModel(name=name, grouptype_id=typeIds['studyGroupId'])
            session.add(studyGroupRecord)
            session.commit()
            RandomizedStudents(faculty, studyGroupRecord, count=random.randint(5, 15))
            pass
        
        def RandomizedTeachers(faculty, department, count=10):
            for _ in range(count):
                teacher = randomUser(mod=faculty.name)
                teacherRecord = UserModel(**teacher)
                session.add(teacherRecord)
                faculty.users.append(teacherRecord)
                department.users.append(teacherRecord)
                allTeachersGroup.users.append(teacherRecord)
            session.commit()
            
        def RandomizedDepartment(faculty, index):
            strs = ['KB', 'BSV', 'ASV', 'ZM', 'IT', 'EL', 'ST', 'GEO', 'MET']
            name = f"{faculty.name}_{index}_{random.choice(strs)}"
            departmentRecord = GroupModel(name=name, grouptype_id=typeIds['departmentTypeId'])
            session.add(departmentRecord)
            session.commit()
            RandomizedTeachers(faculty, departmentRecord, count=random.randint(5, 20))
            pass
        
        def RandomizedFaculty(index):
            facultyGroup = GroupModel(name=f'F{index}', grouptype_id=typeIds['facultyTypeId'])
            session.add(facultyGroup)
            session.commit()
            departmentCount = random.randrange(4, 14)
            for _ in range(departmentCount):
                RandomizedDepartment(facultyGroup, index=_)
            studyGroupCount = random.randrange(20, 40)
            for _ in range(studyGroupCount):
                RandomizedStudyGroup(facultyGroup)
            session.commit()
        
        def RandomizedUniversity():
            facultyCount = random.randrange(3, 7)
            for index in range(facultyCount):
                RandomizedFaculty(index)
            session.commit()
            
        RandomizedUniversity()
        session.commit()
    finally:
        session.close()
