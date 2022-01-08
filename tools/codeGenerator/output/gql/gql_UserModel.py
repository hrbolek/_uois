import graphene
from sqlalchemy.orm import relationship
from BaseModel import BaseModel

def extractSession(info):
    #return info.context['request'].scope['db_session']
    assert not info.context is None, 'Got Bad Context'
    return info.context.get('session')

class UserModel(BaseModel):
    __tablename__ = 'users'
    __table_args__ = {'extend_existing': True} 
    
    eventusermodel_collection = relationship('EventUserModel')
    # eventusermodel_collection = association_proxy('eventusermodel_collection', 'keyword')
    programusermodel_collection = relationship('ProgramUserModel')
    # programusermodel_collection = association_proxy('programusermodel_collection', 'keyword')
    usergroupmodel_collection = relationship('UserGroupModel')
    # usergroupmodel_collection = association_proxy('usergroupmodel_collection', 'keyword')
    rolemodel_collection = relationship('RoleModel')
    # rolemodel_collection = association_proxy('rolemodel_collection', 'keyword')
    subjectusermodel_collection = relationship('SubjectUserModel')
    # subjectusermodel_collection = association_proxy('subjectusermodel_collection', 'keyword')
    studyplanitemteachermodel_collection = relationship('StudyPlanItemTeacherModel')
    # studyplanitemteachermodel_collection = association_proxy('studyplanitemteachermodel_collection', 'keyword')
    subjecttopicusermodel_collection = relationship('SubjectTopicUserModel')
    # subjecttopicusermodel_collection = association_proxy('subjecttopicusermodel_collection', 'keyword')


class get_UserModel(graphene.ObjectType):
    
    id = graphene.String()
    name = graphene.String()
    surname = graphene.String()
    email = graphene.String()
    lastchange = graphene.DateTime()
    externalId = graphene.Int()
    UCO = graphene.String()
    VaVId = graphene.String()
    
        
    eventusermodel_collection = graphene.List('gql_EventUserModel.get_EventUserModel')
        
    def resolver_eventusermodel_collection(parent, info):
        return parent.eventusermodel_collection
        
    programusermodel_collection = graphene.List('gql_ProgramUserModel.get_ProgramUserModel')
        
    def resolver_programusermodel_collection(parent, info):
        return parent.programusermodel_collection
        
    usergroupmodel_collection = graphene.List('gql_UserGroupModel.get_UserGroupModel')
        
    def resolver_usergroupmodel_collection(parent, info):
        return parent.usergroupmodel_collection
        
    rolemodel_collection = graphene.List('gql_RoleModel.get_RoleModel')
        
    def resolver_rolemodel_collection(parent, info):
        return parent.rolemodel_collection
        
    subjectusermodel_collection = graphene.List('gql_SubjectUserModel.get_SubjectUserModel')
        
    def resolver_subjectusermodel_collection(parent, info):
        return parent.subjectusermodel_collection
        
    studyplanitemteachermodel_collection = graphene.List('gql_StudyPlanItemTeacherModel.get_StudyPlanItemTeacherModel')
        
    def resolver_studyplanitemteachermodel_collection(parent, info):
        return parent.studyplanitemteachermodel_collection
        
    subjecttopicusermodel_collection = graphene.List('gql_SubjectTopicUserModel.get_SubjectTopicUserModel')
        
    def resolver_subjecttopicusermodel_collection(parent, info):
        return parent.subjecttopicusermodel_collection


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
    result = graphene.Field('get_UserModel')
    
    def mutate(parent, info, **paramList):
        session = extractSession(info)
        result = UserModel(**paramList)
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
    result = graphene.Field('get_UserModel')
    
    def mutate(parent, info, **paramList):
        session = extractSession(info)
        dbRecord = session.query(UserModel).filter_by(id=paramList['id']).one()
        for key, item in paramList.items():
            if key=='id':
                continue
            setattr(dbRecord, key, item)
        session.commit()
        return update_UserModel(ok=True, result=dbRecord)
    pass


def resolve_users_by_id(root, info, id):
    session = extractSession(info)
    dbRecord = session.query(UserModel).filter_by(id=id).one()
    return dbRecord
def resolve_users_name_starts_with(root, info, name):
    session = extractSession(info)
    dbRecords = session.query(UserModel).filter(UserModel.name.startswith(name)).all()
    return dbRecords
def resolve_users_surname_starts_with(root, info, surname):
    session = extractSession(info)
    dbRecords = session.query(UserModel).filter(UserModel.surname.startswith(surname)).all()
    return dbRecords
def resolve_users_email_starts_with(root, info, email):
    session = extractSession(info)
    dbRecords = session.query(UserModel).filter(UserModel.email.startswith(email)).all()
    return dbRecords
def resolve_users_lastchange_starts_with(root, info, lastchange):
    session = extractSession(info)
    dbRecords = session.query(UserModel).filter(UserModel.lastchange.startswith(lastchange)).all()
    return dbRecords
def resolve_users_externalId_starts_with(root, info, externalId):
    session = extractSession(info)
    dbRecords = session.query(UserModel).filter(UserModel.externalId.startswith(externalId)).all()
    return dbRecords
def resolve_users_UCO_starts_with(root, info, UCO):
    session = extractSession(info)
    dbRecords = session.query(UserModel).filter(UserModel.UCO.startswith(UCO)).all()
    return dbRecords
def resolve_users_VaVId_starts_with(root, info, VaVId):
    session = extractSession(info)
    dbRecords = session.query(UserModel).filter(UserModel.VaVId.startswith(VaVId)).all()
    return dbRecords