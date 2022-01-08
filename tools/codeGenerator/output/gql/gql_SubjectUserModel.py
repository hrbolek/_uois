import graphene
from sqlalchemy.orm import relationship
from BaseModel import BaseModel

def extractSession(info):
    #return info.context['request'].scope['db_session']
    assert not info.context is None, 'Got Bad Context'
    return info.context.get('session')

class SubjectUserModel(BaseModel):
    __tablename__ = 'subjects_users'
    __table_args__ = {'extend_existing': True} 
    
    usermodel = relationship('UserModel')
    # usermodel = association_proxy('usermodel', 'keyword')
    subjectmodel = relationship('SubjectModel')
    # subjectmodel = association_proxy('subjectmodel', 'keyword')
    acreditationuserroletypemodel = relationship('AcreditationUserRoleTypeModel')
    # acreditationuserroletypemodel = association_proxy('acreditationuserroletypemodel', 'keyword')


class get_SubjectUserModel(graphene.ObjectType):
    
    id = graphene.String()
    subject_id = graphene.String()
    user_id = graphene.String()
    roletype_id = graphene.String()
    
        
    usermodel = graphene.Field('gql_UserModel.get_UserModel')
    def resolver_usermodel(parent, info):
        return parent.usermodel
        
    subjectmodel = graphene.Field('gql_SubjectModel.get_SubjectModel')
    def resolver_subjectmodel(parent, info):
        return parent.subjectmodel
        
    acreditationuserroletypemodel = graphene.Field('gql_AcreditationUserRoleTypeModel.get_AcreditationUserRoleTypeModel')
    def resolver_acreditationuserroletypemodel(parent, info):
        return parent.acreditationuserroletypemodel


class create_SubjectUserModel(graphene.Mutation):
    class Arguments:
        id = graphene.String(required=True)
        subject_id = graphene.String(required=True)
        user_id = graphene.String(required=True)
        roletype_id = graphene.String(required=True)

    ok = graphene.Boolean()
    result = graphene.Field('get_SubjectUserModel')
    
    def mutate(parent, info, **paramList):
        session = extractSession(info)
        result = SubjectUserModel(**paramList)
        session.add(result)
        session.commit()
        return create_SubjectUserModel(ok=True, result=result)
    pass

class update_SubjectUserModel(graphene.Mutation):
    class Arguments:
        id = graphene.String(required=True)    
        subject_id = graphene.String(required=False)    
        user_id = graphene.String(required=False)    
        roletype_id = graphene.String(required=False)

    ok = graphene.Boolean()
    result = graphene.Field('get_SubjectUserModel')
    
    def mutate(parent, info, **paramList):
        session = extractSession(info)
        dbRecord = session.query(SubjectUserModel).filter_by(id=paramList['id']).one()
        for key, item in paramList.items():
            if key=='id':
                continue
            setattr(dbRecord, key, item)
        session.commit()
        return update_SubjectUserModel(ok=True, result=dbRecord)
    pass


def resolve_subjects_users_by_id(root, info, id):
    session = extractSession(info)
    dbRecord = session.query(SubjectUserModel).filter_by(id=id).one()
    return dbRecord
def resolve_subjects_users_subject_id_starts_with(root, info, subject_id):
    session = extractSession(info)
    dbRecords = session.query(SubjectUserModel).filter(SubjectUserModel.subject_id.startswith(subject_id)).all()
    return dbRecords
def resolve_subjects_users_user_id_starts_with(root, info, user_id):
    session = extractSession(info)
    dbRecords = session.query(SubjectUserModel).filter(SubjectUserModel.user_id.startswith(user_id)).all()
    return dbRecords
def resolve_subjects_users_roletype_id_starts_with(root, info, roletype_id):
    session = extractSession(info)
    dbRecords = session.query(SubjectUserModel).filter(SubjectUserModel.roletype_id.startswith(roletype_id)).all()
    return dbRecords