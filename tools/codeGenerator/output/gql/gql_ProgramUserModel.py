import graphene
from sqlalchemy.orm import relationship
from BaseModel import BaseModel

def extractSession(info):
    #return info.context['request'].scope['db_session']
    assert not info.context is None, 'Got Bad Context'
    return info.context.get('session')

class ProgramUserModel(BaseModel):
    __tablename__ = 'programs_users'
    __table_args__ = {'extend_existing': True} 
    
    acreditationuserroletypemodel = relationship('AcreditationUserRoleTypeModel')
    # acreditationuserroletypemodel = association_proxy('acreditationuserroletypemodel', 'keyword')
    programmodel = relationship('ProgramModel')
    # programmodel = association_proxy('programmodel', 'keyword')
    usermodel = relationship('UserModel')
    # usermodel = association_proxy('usermodel', 'keyword')


class get_ProgramUserModel(graphene.ObjectType):
    
    id = graphene.String()
    program_id = graphene.String()
    user_id = graphene.String()
    roletype_id = graphene.String()
    
        
    acreditationuserroletypemodel = graphene.Field('gql_AcreditationUserRoleTypeModel.get_AcreditationUserRoleTypeModel')
    def resolver_acreditationuserroletypemodel(parent, info):
        return parent.acreditationuserroletypemodel
        
    programmodel = graphene.Field('gql_ProgramModel.get_ProgramModel')
    def resolver_programmodel(parent, info):
        return parent.programmodel
        
    usermodel = graphene.Field('gql_UserModel.get_UserModel')
    def resolver_usermodel(parent, info):
        return parent.usermodel


class create_ProgramUserModel(graphene.Mutation):
    class Arguments:
        id = graphene.String(required=True)
        program_id = graphene.String(required=True)
        user_id = graphene.String(required=True)
        roletype_id = graphene.String(required=True)

    ok = graphene.Boolean()
    result = graphene.Field('get_ProgramUserModel')
    
    def mutate(parent, info, **paramList):
        session = extractSession(info)
        result = ProgramUserModel(**paramList)
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
    result = graphene.Field('get_ProgramUserModel')
    
    def mutate(parent, info, **paramList):
        session = extractSession(info)
        dbRecord = session.query(ProgramUserModel).filter_by(id=paramList['id']).one()
        for key, item in paramList.items():
            if key=='id':
                continue
            setattr(dbRecord, key, item)
        session.commit()
        return update_ProgramUserModel(ok=True, result=dbRecord)
    pass


def resolve_programs_users_by_id(root, info, id):
    session = extractSession(info)
    dbRecord = session.query(ProgramUserModel).filter_by(id=id).one()
    return dbRecord
def resolve_programs_users_program_id_starts_with(root, info, program_id):
    session = extractSession(info)
    dbRecords = session.query(ProgramUserModel).filter(ProgramUserModel.program_id.startswith(program_id)).all()
    return dbRecords
def resolve_programs_users_user_id_starts_with(root, info, user_id):
    session = extractSession(info)
    dbRecords = session.query(ProgramUserModel).filter(ProgramUserModel.user_id.startswith(user_id)).all()
    return dbRecords
def resolve_programs_users_roletype_id_starts_with(root, info, roletype_id):
    session = extractSession(info)
    dbRecords = session.query(ProgramUserModel).filter(ProgramUserModel.roletype_id.startswith(roletype_id)).all()
    return dbRecords