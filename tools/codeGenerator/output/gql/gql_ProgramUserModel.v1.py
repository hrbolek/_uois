import graphene
from sqlalchemy.orm import relationship
from BaseModel import BaseModel

def extractSession(info):
    #return info.context['request'].scope['db_session']
    assert not info.context is None, 'Got Bad Context'
    return info.context.get('session')

class ProgramUserModelEx(BaseModel):
    __tablename__ = 'programs_users'
    __table_args__ = {'extend_existing': True} 
    
    acreditationuserroletypemodel = relationship('AcreditationUserRoleTypeModelEx')
    # acreditationuserroletypemodel = association_proxy('acreditationuserroletypemodel', 'keyword')
    programmodel = relationship('ProgramModelEx')
    # programmodel = association_proxy('programmodel', 'keyword')
    usermodel = relationship('UserModelEx')
    # usermodel = association_proxy('usermodel', 'keyword')


class ProgramUserModel(graphene.ObjectType):
    
    id = graphene.String()
    program_id = graphene.String()
    user_id = graphene.String()
    roletype_id = graphene.String()
    
        
    acreditationuserroletypemodel = graphene.Field('graphqltypes.gql_AcreditationUserRoleTypeModel.AcreditationUserRoleTypeModel')
    def resolver_acreditationuserroletypemodel(parent, info):
        return parent.acreditationuserroletypemodel
        
    programmodel = graphene.Field('graphqltypes.gql_ProgramModel.ProgramModel')
    def resolver_programmodel(parent, info):
        return parent.programmodel
        
    usermodel = graphene.Field('graphqltypes.gql_UserModel.UserModel')
    def resolver_usermodel(parent, info):
        return parent.usermodel


class create_ProgramUserModel(graphene.Mutation):
    class Arguments:
        id = graphene.String(required=True)
        program_id = graphene.String(required=True)
        user_id = graphene.String(required=True)
        roletype_id = graphene.String(required=True)

    ok = graphene.Boolean()
    result = graphene.Field('graphqltypes.gql_ProgramUserModel.ProgramUserModel')
    
    def mutate(parent, info, **paramList):
        session = extractSession(info)
        result = ProgramUserModelEx(**paramList)
        session.add(result)
        session.commit()
        return create_ProgramUserModel(ok=True, result=result)
    pass

class update_ProgramUserModel(graphene.Mutation):
    class Arguments:
        id = graphene.String(required=True)    
        program_id = graphene.String(required=False)    
        user_id = graphene.String(required=False)    
        roletype_id = graphene.String(required=False)

    ok = graphene.Boolean()
    result = graphene.Field('graphqltypes.gql_ProgramUserModel.ProgramUserModel')
    
    def mutate(parent, info, **paramList):
        session = extractSession(info)
        dbRecord = session.query(ProgramUserModelEx).filter_by(id=paramList['id']).one()
        for key, item in paramList.items():
            if key=='id':
                continue
            setattr(dbRecord, key, item)
        session.commit()
        return update_ProgramUserModel(ok=True, result=dbRecord)
    pass

def to_dict(row):
    return {column.name: getattr(row, row.__mapper__.get_property_by_column(column).key) for column in row.__table__.columns}


def resolve_programs_users_by_id(root, info, id):
    try:
        session = extractSession(info)
        dbRecord = session.query(ProgramUserModelEx).filter_by(id=id).one()
    except Exception as e:
        print('An error occured (by_id)')
        print(e)
    print(f'to_dict(dbRecord)')
    return dbRecord
def resolve_programs_users_program_id_starts_with(root, info, program_id):
    try:
        session = extractSession(info)
        dbRecords = session.query(ProgramUserModelEx).filter(ProgramUserModel.program_id.startswith(program_id)).all()
    except Exception as e:
        print('An error occured (startswith)')
        print(e)
    return dbRecords
def resolve_programs_users_user_id_starts_with(root, info, user_id):
    try:
        session = extractSession(info)
        dbRecords = session.query(ProgramUserModelEx).filter(ProgramUserModel.user_id.startswith(user_id)).all()
    except Exception as e:
        print('An error occured (startswith)')
        print(e)
    return dbRecords
def resolve_programs_users_roletype_id_starts_with(root, info, roletype_id):
    try:
        session = extractSession(info)
        dbRecords = session.query(ProgramUserModelEx).filter(ProgramUserModel.roletype_id.startswith(roletype_id)).all()
    except Exception as e:
        print('An error occured (startswith)')
        print(e)
    return dbRecords