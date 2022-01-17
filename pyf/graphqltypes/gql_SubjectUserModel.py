import graphene
from sqlalchemy.orm import relationship
from BaseModel import BaseModel

def extractSession(info):
    #return info.context['request'].scope['db_session']
    assert not info.context is None, 'Got Bad Context'
    return info.context.get('session')

class SubjectUserModelEx(BaseModel):
    __tablename__ = 'subjects_users'
    __table_args__ = {'extend_existing': True} 
    
    usermodel = relationship('UserModelEx')
    # usermodel = association_proxy('usermodel', 'keyword')
    subjectmodel = relationship('SubjectModelEx')
    # subjectmodel = association_proxy('subjectmodel', 'keyword')
    acreditationuserroletypemodel = relationship('AcreditationUserRoleTypeModelEx')
    # acreditationuserroletypemodel = association_proxy('acreditationuserroletypemodel', 'keyword')


class SubjectUserModel(graphene.ObjectType):
    
    id = graphene.String()
    subject_id = graphene.String()
    user_id = graphene.String()
    roletype_id = graphene.String()
    
        
    usermodel = graphene.Field('graphqltypes.gql_UserModel.UserModel')
    def resolver_usermodel(parent, info):
        return parent.usermodel
        
    subjectmodel = graphene.Field('graphqltypes.gql_SubjectModel.SubjectModel')
    def resolver_subjectmodel(parent, info):
        return parent.subjectmodel
        
    acreditationuserroletypemodel = graphene.Field('graphqltypes.gql_AcreditationUserRoleTypeModel.AcreditationUserRoleTypeModel')
    def resolver_acreditationuserroletypemodel(parent, info):
        return parent.acreditationuserroletypemodel


class create_SubjectUserModel(graphene.Mutation):
    class Arguments:
        id = graphene.String(required=True)
        subject_id = graphene.String(required=True)
        user_id = graphene.String(required=True)
        roletype_id = graphene.String(required=True)

    ok = graphene.Boolean()
    result = graphene.Field('graphqltypes.gql_SubjectUserModel.SubjectUserModel')
    
    def mutate(parent, info, **paramList):
        session = extractSession(info)
        result = SubjectUserModelEx(**paramList)
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
    result = graphene.Field('graphqltypes.gql_SubjectUserModel.SubjectUserModel')
    
    def mutate(parent, info, **paramList):
        session = extractSession(info)
        dbRecord = session.query(SubjectUserModelEx).filter_by(id=paramList['id']).one()
        for key, item in paramList.items():
            if key=='id':
                continue
            setattr(dbRecord, key, item)
        session.commit()
        return update_SubjectUserModel(ok=True, result=dbRecord)
    pass

def to_dict(row):
    return {column.name: getattr(row, row.__mapper__.get_property_by_column(column).key) for column in row.__table__.columns}


def resolve_subjects_users_by_id(root, info, id):
    try:
        session = extractSession(info)
        dbRecord = session.query(SubjectUserModelEx).filter_by(id=id).one()
    except Exception as e:
        print('An error occured (by_id)')
        print(e)
    print(f'to_dict(dbRecord)')
    return dbRecord
def resolve_subjects_users_subject_id_starts_with(root, info, subject_id):
    try:
        session = extractSession(info)
        dbRecords = session.query(SubjectUserModelEx).filter(SubjectUserModel.subject_id.startswith(subject_id)).all()
    except Exception as e:
        print('An error occured (startswith)')
        print(e)
    return dbRecords
def resolve_subjects_users_user_id_starts_with(root, info, user_id):
    try:
        session = extractSession(info)
        dbRecords = session.query(SubjectUserModelEx).filter(SubjectUserModel.user_id.startswith(user_id)).all()
    except Exception as e:
        print('An error occured (startswith)')
        print(e)
    return dbRecords
def resolve_subjects_users_roletype_id_starts_with(root, info, roletype_id):
    try:
        session = extractSession(info)
        dbRecords = session.query(SubjectUserModelEx).filter(SubjectUserModel.roletype_id.startswith(roletype_id)).all()
    except Exception as e:
        print('An error occured (startswith)')
        print(e)
    return dbRecords