from typing_extensions import Required

#from sqlalchemy.sql.sqltypes import Boolean
from graphene import ObjectType, String, Field, ID, List, DateTime, Mutation, Boolean, Int, NonNull

from models.GroupRelated.GroupModel import GroupModel
from models.GroupRelated.UserModel import UserModel
from models.GroupRelated.RoleModel import RoleModel

from graphqltypes.Utils import extractSession

from graphqltypes.Utils import createRootResolverById, createRootResolverByName

GroupRootResolverById = createRootResolverById(GroupModel)
GroupRootResolverByName = createRootResolverByName(GroupModel)


class AddUser(Mutation):
    """Adds a user to this group"""
    class Arguments():
        userid = ID()

    ok = Boolean()
    result = Field('graphqltypes.User.UserType')
    msg = String()

    def mutate(parent, info, userid):
        session = extractSession(info)
        groupRecord = session.query(GroupModel).filter_by(id=parent.id).one()
        userIsIn = False
        for item in groupRecord.users:
            if item.id == userIsIn:
                userIsIn = True
                break
        
        if userIsIn:
            return AddUser(ok=False, result=item, msg=f'User {userid} is already in this group')
        
        userRecord = session.query(UserModel).filter_by(id=userid).one()
        groupRecord.users.append(userRecord)
        session.commit()
        result = userRecord
        return AddUser(ok=True, result=result, msg='')

class RemoveUser(Mutation):
    """Removes a user from this group
    
    Parameters
    ----------
    userid: ID()
        identification of user which have to be removed from group
    """
    class Arguments():
        userid = ID()

    ok = Boolean()
    result = Field('graphqltypes.User.UserType')
    msg = String()

    def mutate(parent, info, userid):
        session = extractSession(info)
        groupRecord = session.query(GroupModel).filter_by(id=parent.id).one()
        userIsIn = False
        for item in groupRecord.users:
            if item.id == userIsIn:
                userIsIn = True
                break
        
        if userIsIn:
            groupRecord.users.remove(item)
            session.commit()
            return AddUser(ok=True, result=item, msg=f'User {userid} has been successfuly removed from this group {parent.id}')

        userRecord = session.query(UserModel).filter_by(id=userid).one()
        return AddUser(ok=False, result=userRecord, msg=f'User {userid} is not member of this group {parent.id}')

class PromoteUser(Mutation):
    """Gives a user a role in this group"""
    class Arguments():
        userid = ID()
        roletypeid = ID()

    ok = Boolean()
    result = Field('graphqltypes.User.UserType')
    msg = String()

    def mutate(parent, info, userid, roletypeid):
        session = extractSession(info)
        groupRecord = session.query(GroupModel).filter_by(id=parent.id).one()
        userIsIn = False
        for item in groupRecord.users:
            if item.id == userIsIn:
                userIsIn = True
                break
        
        if not userIsIn:
            return PromoteUser(ok=False, result=item, msg='User is not in group')

        userHasRole = False
        for role in groupRecord.roles:
            if not item.user_id == userid:
                continue
            if role.roletype_id == roletypeid:
                userHasRole = True
                break
        
        if userHasRole:
            return PromoteUser(ok=False, result=item, msg='User has already this role')

        newRole = RoleModel(group=groupRecord, user=item, roletypeid=roletypeid)
        session.add(newRole)
        session.commit()

        return PromoteUser(ok=False, result=item, msg='')

class DemoteUser(Mutation):
    """Removes a role of user in the group"""
    class Arguments():
        userid = ID()
        roletypeid = ID()

    ok = Boolean()
    msg = String()
    result = Field('graphqltypes.User.UserType')

    def mutate(parent, info, userid, roletypeid):
        session = extractSession(info)
        groupRecord = session.query(GroupModel).filter_by(id=parent.id).one()
        userIsIn = False
        for item in groupRecord.users:
            if item.id == userIsIn:
                userIsIn = True
                break
        
        if not userIsIn:
            return DemoteUser(ok=False, result=item, msg=f'User {userid} is not in group {parent.id}')

        userHasRole = False
        for role in groupRecord.roles:
            if not role.user_id == userid:
                continue
            if role.roletype_id == roletypeid:
                userHasRole = True
                break
        
        if not userHasRole:
            return DemoteUser(ok=False, result=item, msg=f'User {userid} has not role {roletypeid}')

        session.delete(role)
        session.commit()

        return DemoteUser(ok=False, result=item, msg='')

class GroupType(ObjectType):
    """Represent a group of users"""

    id = ID()
    name = String()

    lastchange = DateTime()
    externalId = String()

    grouptype_id = Int()

    add_user = AddUser.Field()
    remove_user = RemoveUser.Field()
    promote_user = PromoteUser.Field()
    demote_user = DemoteUser.Field()
    
    #users = List(Field('graphqltypes.User.UserType').type)
    users = List('graphqltypes.User.UserType')
    #users = List(lambda:Field('graphqltypes.User.UserType').type)
    def resolve_users(parent, info):
        session = extractSession(info)
        groupRecord = session.query(GroupModel).get(parent.id)
        return groupRecord.users
        
def resolve_groups_by_type(root, info, type_id):
    print('@resolve_groups_by_type', type_id)
    session = extractSession(info)
    result = session.query(GroupModel).filter(GroupModel.grouptype_id==type_id).all()
    return result



from models.GroupRelated.GroupTypeModel import GroupTypeModel
from models.GroupRelated.RoleTypeModel import RoleTypeModel

def ensureData(session=None):
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

    try:
        departmentTypeId = ensureDataItem(session, GroupTypeModel, 'department')
        facultyTypeId = ensureDataItem(session, GroupTypeModel, 'faculty')
        studyGroupId =  ensureDataItem(session, GroupTypeModel, 'studygroup')
        universityTypeId = ensureDataItem(session, GroupTypeModel, 'university')

        departmentHeadRoleTypeId = ensureDataItem(session, RoleTypeModel, 'head of department')
        deanRoleTypeId = ensureDataItem(session, RoleTypeModel, 'dean')
        viceDeanRoleTypeId = ensureDataItem(session, RoleTypeModel, 'vice dean')
        rectorRoleTypeId = ensureDataItem(session, RoleTypeModel, 'rector')
        viceRectorRoleTypeId = ensureDataItem(session, RoleTypeModel, 'vice rector')

        result = {
            'departmentTypeId': departmentTypeId,
            'facultyTypeId': facultyTypeId,
            'studyGroupId': studyGroupId,
            'universityTypeId': universityTypeId,
            'departmentHeadRoleTypeId': departmentHeadRoleTypeId,
            'deanRoleTypeId': deanRoleTypeId,
            'viceDeanRoleTypeId': viceDeanRoleTypeId,
            'rectorRoleTypeId': rectorRoleTypeId,
            'viceRectorRoleTypeId': viceRectorRoleTypeId
        }    
    finally:
        session.close()
    return result

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

from models.GroupRelated.UserModel import UserModel
from models.GroupRelated.RoleModel import RoleModel

class CreateRandomUniversity(Mutation):
    class Arguments():
        facultyCount = Int()
        name = String()
        pass

    result = Field('graphqltypes.Group.GroupType')
    ok = Boolean()

    def mutate(root, info, name='University', facultyCount=5):
        session = extractSession(info)

        try:
            
            typeIds = ensureData(session=session)
            
            allTeachersGroup = GroupModel(name=f'{name}.AllTeachers')
            allStudentsGroup = GroupModel(name=f'{name}.AllStudents')

            session.add(allTeachersGroup)
            session.add(allStudentsGroup)
            session.commit()
            
            def RandomizedStudents(university, faculty, studyGroup, count=10):
                for _ in range(count):
                    student = randomUser(mod=faculty.name)
                    studentRecord = UserModel(**student)
                    session.add(studentRecord)
                    faculty.users.append(studentRecord)
                    studyGroup.users.append(studentRecord)
                    allStudentsGroup.users.append(studentRecord)
                    university.users.append(studentRecord)
                session.commit()
            
            def RandomizedStudyGroup(university, faculty):
                strs = ['KB', 'BSV', 'ASV', 'ZM', 'IT', 'EL', 'ST', 'GEO', 'MET']
                appendixes = ['', '-K', '-C', '-O', '-V', '-X']
                name = f"{faculty.name}-5-{random.choice([1, 2, 3, 4, 5])}{random.choice(strs)}{random.choice(appendixes)}"
                studyGroupRecord = GroupModel(name=name, grouptype_id=typeIds['studyGroupId'])
                session.add(studyGroupRecord)
                session.commit()
                RandomizedStudents(university, faculty, studyGroupRecord, count=random.randint(5, 15))
                return studyGroupRecord
            
            def RandomizedTeachers(university, faculty, department, count=10):
                for _ in range(count):
                    teacher = randomUser(mod=faculty.name)
                    teacherRecord = UserModel(**teacher)
                    session.add(teacherRecord)
                    faculty.users.append(teacherRecord)
                    department.users.append(teacherRecord)
                    allTeachersGroup.users.append(teacherRecord)
                    university.users.append(teacherRecord)
                session.commit()
                
            def RandomizedDepartment(university, faculty, index):
                strs = ['KB', 'BSV', 'ASV', 'ZM', 'IT', 'EL', 'ST', 'GEO', 'MET']
                name = f"{faculty.name}_{index}_{random.choice(strs)}"
                departmentRecord = GroupModel(name=name, grouptype_id=typeIds['departmentTypeId'])
                session.add(departmentRecord)
                session.commit()
                RandomizedTeachers(university, faculty, departmentRecord, count=random.randint(5, 20))
                rolerecord = RoleModel(user=departmentRecord.users[0], group=departmentRecord, roletype_id=typeIds['departmentHeadRoleTypeId'])
                session.add(rolerecord)
                departmentRecord.roles.append(rolerecord)
                session.commit()
                return departmentRecord
            
            def RandomizedFaculty(university, index):
                print('@begin of RandomizedFaculty')
                facultyGroup = GroupModel(name=f'F{index}', grouptype_id=typeIds['facultyTypeId'])
                session.add(facultyGroup)
                session.commit()
                departmentCount = random.randrange(4, 14)
                for _ in range(departmentCount):
                    RandomizedDepartment(university, facultyGroup, index=_)
                studyGroupCount = random.randrange(20, 40)
                for _ in range(studyGroupCount):
                    RandomizedStudyGroup(university, facultyGroup)
                session.commit()
                rolerecord = RoleModel(user=facultyGroup.users[0], group=facultyGroup, roletype_id=typeIds['deanRoleTypeId'])
                session.add(rolerecord)
                facultyGroup.roles.append(rolerecord)
                session.commit()
                print('@end of RandomizedFaculty')
                return facultyGroup
            
            def RandomizedUniversity(facultyCount):
                print('@begin of RandomizedUniversity')
                universityGroup = GroupModel(name=name, grouptype_id=typeIds['universityTypeId'])
                session.add(universityGroup)
                session.commit()
                
                for index in range(facultyCount):
                    RandomizedFaculty(universityGroup, index+1)

                session.commit()
                print('@end of RandomizedUniversity', universityGroup.id)
                return universityGroup
                
            result = RandomizedUniversity(facultyCount)
            print(result.id)
        except Exception as e:
            print('An error occured @CreateRandomUniversity')
            print(e)
        finally:
            session.close()    
        pass
        
        print('Created', name, result)
        return CreateRandomUniversity(ok=True, result=result)

    pass

"""
mutation {
  createRandomUniversity(facultyCount: 2, name: "University") {
    ok
    result {
      id
      name
    }
  }
}

query {
  group(id: 13)
  {
    id
    name
    users {
      id
      name
      email
    }
  }
}
"""