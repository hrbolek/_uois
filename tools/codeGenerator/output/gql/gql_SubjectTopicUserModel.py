import graphene
from sqlalchemy.orm import relationship
from BaseModel import BaseModel

def extractSession(info):
    #return info.context['request'].scope['db_session']
    assert not info.context is None, 'Got Bad Context'
    return info.context.get('session')

class SubjectTopicUserModel(BaseModel):
    __tablename__ = 'subjecttopics_users'
    __table_args__ = {'extend_existing': True} 
    
    subjecttopicmodel = relationship('SubjectTopicModel')
    # subjecttopicmodel = association_proxy('subjecttopicmodel', 'keyword')
    usermodel = relationship('UserModel')
    # usermodel = association_proxy('usermodel', 'keyword')
    acreditationuserroletypemodel = relationship('AcreditationUserRoleTypeModel')
    # acreditationuserroletypemodel = association_proxy('acreditationuserroletypemodel', 'keyword')


class get_SubjectTopicUserModel(graphene.ObjectType):
    
    id = graphene.String()
    subjecttopic_id = graphene.String()
    user_id = graphene.String()
    roletype_id = graphene.String()
    
        
    subjecttopicmodel = graphene.Field('gql_SubjectTopicModel.get_SubjectTopicModel')
    def resolver_subjecttopicmodel(parent, info):
        return parent.subjecttopicmodel
        
    usermodel = graphene.Field('gql_UserModel.get_UserModel')
    def resolver_usermodel(parent, info):
        return parent.usermodel
        
    acreditationuserroletypemodel = graphene.Field('gql_AcreditationUserRoleTypeModel.get_AcreditationUserRoleTypeModel')
    def resolver_acreditationuserroletypemodel(parent, info):
        return parent.acreditationuserroletypemodel


class create_SubjectTopicUserModel(graphene.Mutation):
    class Arguments:
        id = graphene.String(required=True)
        subjecttopic_id = graphene.String(required=True)
        user_id = graphene.String(required=True)
        roletype_id = graphene.String(required=True)

    ok = graphene.Boolean()
    result = graphene.Field('get_SubjectTopicUserModel')
    
    def mutate(parent, info, **paramList):
        session = extractSession(info)
        result = SubjectTopicUserModel(**paramList)
        session.add(result)
        session.commit()
        return create_SubjectTopicUserModel(ok=True, result=result)
    pass

class update_SubjectTopicUserModel(graphene.Mutation):
    class Arguments:
        id = graphene.String(required=True)    
        subjecttopic_id = graphene.String(required=False)    
        user_id = graphene.String(required=False)    
        roletype_id = graphene.String(required=False)

    ok = graphene.Boolean()
    result = graphene.Field('get_SubjectTopicUserModel')
    
    def mutate(parent, info, **paramList):
        session = extractSession(info)
        dbRecord = session.query(SubjectTopicUserModel).filter_by(id=paramList['id']).one()
        for key, item in paramList.items():
            if key=='id':
                continue
            setattr(dbRecord, key, item)
        session.commit()
        return update_SubjectTopicUserModel(ok=True, result=dbRecord)
    pass


def resolve_subjecttopics_users_by_id(root, info, id):
    session = extractSession(info)
    dbRecord = session.query(SubjectTopicUserModel).filter_by(id=id).one()
    return dbRecord
def resolve_subjecttopics_users_subjecttopic_id_starts_with(root, info, subjecttopic_id):
    session = extractSession(info)
    dbRecords = session.query(SubjectTopicUserModel).filter(SubjectTopicUserModel.subjecttopic_id.startswith(subjecttopic_id)).all()
    return dbRecords
def resolve_subjecttopics_users_user_id_starts_with(root, info, user_id):
    session = extractSession(info)
    dbRecords = session.query(SubjectTopicUserModel).filter(SubjectTopicUserModel.user_id.startswith(user_id)).all()
    return dbRecords
def resolve_subjecttopics_users_roletype_id_starts_with(root, info, roletype_id):
    session = extractSession(info)
    dbRecords = session.query(SubjectTopicUserModel).filter(SubjectTopicUserModel.roletype_id.startswith(roletype_id)).all()
    return dbRecords