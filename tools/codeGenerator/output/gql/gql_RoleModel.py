import graphene
from sqlalchemy.orm import relationship
from BaseModel import BaseModel

def extractSession(info):
    #return info.context['request'].scope['db_session']
    assert not info.context is None, 'Got Bad Context'
    return info.context.get('session')

class RoleModel(BaseModel):
    __tablename__ = 'roles'
    __table_args__ = {'extend_existing': True} 
    
    usermodel = relationship('UserModel')
    # usermodel = association_proxy('usermodel', 'keyword')
    roletypemodel = relationship('RoleTypeModel')
    # roletypemodel = association_proxy('roletypemodel', 'keyword')
    groupmodel = relationship('GroupModel')
    # groupmodel = association_proxy('groupmodel', 'keyword')


class get_RoleModel(graphene.ObjectType):
    
    id = graphene.String()
    name = graphene.String()
    lastchange = graphene.DateTime()
    roletype_id = graphene.String()
    user_id = graphene.String()
    group_id = graphene.String()
    
        
    usermodel = graphene.Field('gql_UserModel.get_UserModel')
    def resolver_usermodel(parent, info):
        return parent.usermodel
        
    roletypemodel = graphene.Field('gql_RoleTypeModel.get_RoleTypeModel')
    def resolver_roletypemodel(parent, info):
        return parent.roletypemodel
        
    groupmodel = graphene.Field('gql_GroupModel.get_GroupModel')
    def resolver_groupmodel(parent, info):
        return parent.groupmodel


class create_RoleModel(graphene.Mutation):
    class Arguments:
        id = graphene.String(required=True)
        name = graphene.String(required=True)
        lastchange = graphene.DateTime(required=True)
        roletype_id = graphene.String(required=True)
        user_id = graphene.String(required=True)
        group_id = graphene.String(required=True)

    ok = graphene.Boolean()
    result = graphene.Field('get_RoleModel')
    
    def mutate(parent, info, **paramList):
        session = extractSession(info)
        result = RoleModel(**paramList)
        session.add(result)
        session.commit()
        return create_RoleModel(ok=True, result=result)
    pass

class update_RoleModel(graphene.Mutation):
    class Arguments:
        id = graphene.String(required=True)    
        name = graphene.String(required=False)    
        lastchange = graphene.DateTime(required=False)    
        roletype_id = graphene.String(required=False)    
        user_id = graphene.String(required=False)    
        group_id = graphene.String(required=False)

    ok = graphene.Boolean()
    result = graphene.Field('get_RoleModel')
    
    def mutate(parent, info, **paramList):
        session = extractSession(info)
        dbRecord = session.query(RoleModel).filter_by(id=paramList['id']).one()
        for key, item in paramList.items():
            if key=='id':
                continue
            setattr(dbRecord, key, item)
        session.commit()
        return update_RoleModel(ok=True, result=dbRecord)
    pass


def resolve_roles_by_id(root, info, id):
    session = extractSession(info)
    dbRecord = session.query(RoleModel).filter_by(id=id).one()
    return dbRecord
def resolve_roles_name_starts_with(root, info, name):
    session = extractSession(info)
    dbRecords = session.query(RoleModel).filter(RoleModel.name.startswith(name)).all()
    return dbRecords
def resolve_roles_lastchange_starts_with(root, info, lastchange):
    session = extractSession(info)
    dbRecords = session.query(RoleModel).filter(RoleModel.lastchange.startswith(lastchange)).all()
    return dbRecords
def resolve_roles_roletype_id_starts_with(root, info, roletype_id):
    session = extractSession(info)
    dbRecords = session.query(RoleModel).filter(RoleModel.roletype_id.startswith(roletype_id)).all()
    return dbRecords
def resolve_roles_user_id_starts_with(root, info, user_id):
    session = extractSession(info)
    dbRecords = session.query(RoleModel).filter(RoleModel.user_id.startswith(user_id)).all()
    return dbRecords
def resolve_roles_group_id_starts_with(root, info, group_id):
    session = extractSession(info)
    dbRecords = session.query(RoleModel).filter(RoleModel.group_id.startswith(group_id)).all()
    return dbRecords