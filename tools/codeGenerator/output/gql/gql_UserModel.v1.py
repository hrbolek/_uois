import graphene
from sqlalchemy.orm import relationship
from BaseModel import BaseModel

def extractSession(info):
    #return info.context['request'].scope['db_session']
    assert not info.context is None, 'Got Bad Context'
    return info.context.get('session')

class UserModelEx(BaseModel):
    __tablename__ = 'users'
    __table_args__ = {'extend_existing': True} 
    
    eventusermodels = relationship('EventUserModelEx')
    # eventusermodels = association_proxy('eventusermodels', 'keyword')
    programusermodels = relationship('ProgramUserModelEx')
    # programusermodels = association_proxy('programusermodels', 'keyword')
    usergroupmodels = relationship('UserGroupModelEx')
    # usergroupmodels = association_proxy('usergroupmodels', 'keyword')
    rolemodels = relationship('RoleModelEx')
    # rolemodels = association_proxy('rolemodels', 'keyword')
    subjectusermodels = relationship('SubjectUserModelEx')
    # subjectusermodels = association_proxy('subjectusermodels', 'keyword')
    studyplanitemteachermodels = relationship('StudyPlanItemTeacherModelEx')
    # studyplanitemteachermodels = association_proxy('studyplanitemteachermodels', 'keyword')
    subjecttopicusermodels = relationship('SubjectTopicUserModelEx')
    # subjecttopicusermodels = association_proxy('subjecttopicusermodels', 'keyword')


class UserModel(graphene.ObjectType):
    
    id = graphene.String()
    name = graphene.String()
    surname = graphene.String()
    email = graphene.String()
    lastchange = graphene.DateTime()
    externalId = graphene.Int()
    UCO = graphene.String()
    VaVId = graphene.String()
    
        
    eventusermodels = graphene.List('graphqltypes.gql_EventUserModel.EventUserModel')
        
    def resolver_eventusermodels(parent, info):
        return parent.eventusermodels
        
    programusermodels = graphene.List('graphqltypes.gql_ProgramUserModel.ProgramUserModel')
        
    def resolver_programusermodels(parent, info):
        return parent.programusermodels
        
    usergroupmodels = graphene.List('graphqltypes.gql_UserGroupModel.UserGroupModel')
        
    def resolver_usergroupmodels(parent, info):
        return parent.usergroupmodels
        
    rolemodels = graphene.List('graphqltypes.gql_RoleModel.RoleModel')
        
    def resolver_rolemodels(parent, info):
        return parent.rolemodels
        
    subjectusermodels = graphene.List('graphqltypes.gql_SubjectUserModel.SubjectUserModel')
        
    def resolver_subjectusermodels(parent, info):
        return parent.subjectusermodels
        
    studyplanitemteachermodels = graphene.List('graphqltypes.gql_StudyPlanItemTeacherModel.StudyPlanItemTeacherModel')
        
    def resolver_studyplanitemteachermodels(parent, info):
        return parent.studyplanitemteachermodels
        
    subjecttopicusermodels = graphene.List('graphqltypes.gql_SubjectTopicUserModel.SubjectTopicUserModel')
        
    def resolver_subjecttopicusermodels(parent, info):
        return parent.subjecttopicusermodels


class create_UserModel(graphene.Mutation):
    class Arguments:
        id = graphene.String(required=True)
        name = graphene.String(required=True)
        surname = graphene.String(required=True)
        email = graphene.String(required=True)
        lastchange = graphene.DateTime(required=True)
        externalId = graphene.Int(required=True)
        UCO = graphene.String(required=True)
        VaVId = graphene.String(required=True)

    ok = graphene.Boolean()
    result = graphene.Field('graphqltypes.gql_UserModel.UserModel')
    
    def mutate(parent, info, **paramList):
        session = extractSession(info)
        result = UserModelEx(**paramList)
        session.add(result)
        session.commit()
        return create_UserModel(ok=True, result=result)
    pass

class update_UserModel(graphene.Mutation):
    class Arguments:
        id = graphene.String(required=True)    
        name = graphene.String(required=False)    
        surname = graphene.String(required=False)    
        email = graphene.String(required=False)    
        lastchange = graphene.DateTime(required=False)    
        externalId = graphene.Int(required=False)    
        UCO = graphene.String(required=False)    
        VaVId = graphene.String(required=False)

    ok = graphene.Boolean()
    result = graphene.Field('graphqltypes.gql_UserModel.UserModel')
    
    def mutate(parent, info, **paramList):
        session = extractSession(info)
        dbRecord = session.query(UserModelEx).filter_by(id=paramList['id']).one()
        for key, item in paramList.items():
            if key=='id':
                continue
            setattr(dbRecord, key, item)
        session.commit()
        return update_UserModel(ok=True, result=dbRecord)
    pass

def to_dict(row):
    return {column.name: getattr(row, row.__mapper__.get_property_by_column(column).key) for column in row.__table__.columns}


def resolve_users_by_id(root, info, id):
    try:
        session = extractSession(info)
        dbRecord = session.query(UserModelEx).filter_by(id=id).one()
    except Exception as e:
        print('An error occured (by_id)')
        print(e)
    print(f'to_dict(dbRecord)')
    return dbRecord
def resolve_users_name_starts_with(root, info, name):
    try:
        session = extractSession(info)
        dbRecords = session.query(UserModelEx).filter(UserModel.name.startswith(name)).all()
    except Exception as e:
        print('An error occured (startswith)')
        print(e)
    return dbRecords
def resolve_users_surname_starts_with(root, info, surname):
    try:
        session = extractSession(info)
        dbRecords = session.query(UserModelEx).filter(UserModel.surname.startswith(surname)).all()
    except Exception as e:
        print('An error occured (startswith)')
        print(e)
    return dbRecords
def resolve_users_email_starts_with(root, info, email):
    try:
        session = extractSession(info)
        dbRecords = session.query(UserModelEx).filter(UserModel.email.startswith(email)).all()
    except Exception as e:
        print('An error occured (startswith)')
        print(e)
    return dbRecords
def resolve_users_lastchange_starts_with(root, info, lastchange):
    try:
        session = extractSession(info)
        dbRecords = session.query(UserModelEx).filter(UserModel.lastchange.startswith(lastchange)).all()
    except Exception as e:
        print('An error occured (startswith)')
        print(e)
    return dbRecords
def resolve_users_externalId_starts_with(root, info, externalId):
    try:
        session = extractSession(info)
        dbRecords = session.query(UserModelEx).filter(UserModel.externalId.startswith(externalId)).all()
    except Exception as e:
        print('An error occured (startswith)')
        print(e)
    return dbRecords
def resolve_users_UCO_starts_with(root, info, UCO):
    try:
        session = extractSession(info)
        dbRecords = session.query(UserModelEx).filter(UserModel.UCO.startswith(UCO)).all()
    except Exception as e:
        print('An error occured (startswith)')
        print(e)
    return dbRecords
def resolve_users_VaVId_starts_with(root, info, VaVId):
    try:
        session = extractSession(info)
        dbRecords = session.query(UserModelEx).filter(UserModel.VaVId.startswith(VaVId)).all()
    except Exception as e:
        print('An error occured (startswith)')
        print(e)
    return dbRecords