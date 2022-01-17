import graphene
from sqlalchemy.orm import relationship
from BaseModel import BaseModel

def extractSession(info):
    #return info.context['request'].scope['db_session']
    assert not info.context is None, 'Got Bad Context'
    return info.context.get('session')

class RoleModelEx(BaseModel):
    __tablename__ = 'roles'
    __table_args__ = {'extend_existing': True} 
    
    usermodel = relationship('UserModelEx')
    # usermodel = association_proxy('usermodel', 'keyword')
    roletypemodel = relationship('RoleTypeModelEx')
    # roletypemodel = association_proxy('roletypemodel', 'keyword')
    groupmodel = relationship('GroupModelEx')
    # groupmodel = association_proxy('groupmodel', 'keyword')


class RoleModel(graphene.ObjectType):
    
    id = graphene.String()
    name = graphene.String()
    lastchange = graphene.DateTime()
    roletype_id = graphene.String()
    user_id = graphene.String()
    group_id = graphene.String()
    
        
    usermodel = graphene.Field('graphqltypes.gql_UserModel.UserModel')
    def resolver_usermodel(parent, info):
        return parent.usermodel
        
    roletypemodel = graphene.Field('graphqltypes.gql_RoleTypeModel.RoleTypeModel')
    def resolver_roletypemodel(parent, info):
        return parent.roletypemodel
        
    groupmodel = graphene.Field('graphqltypes.gql_GroupModel.GroupModel')
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
    result = graphene.Field('graphqltypes.gql_RoleModel.RoleModel')
    
    def mutate(parent, info, **paramList):
        session = extractSession(info)
        result = RoleModelEx(**paramList)
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
    result = graphene.Field('graphqltypes.gql_RoleModel.RoleModel')
    
    def mutate(parent, info, **paramList):
        session = extractSession(info)
        dbRecord = session.query(RoleModelEx).filter_by(id=paramList['id']).one()
        for key, item in paramList.items():
            if key=='id':
                continue
            setattr(dbRecord, key, item)
        session.commit()
        return update_RoleModel(ok=True, result=dbRecord)
    pass

def to_dict(row):
    return {column.name: getattr(row, row.__mapper__.get_property_by_column(column).key) for column in row.__table__.columns}


def resolve_roles_by_id(root, info, id):
    try:
        session = extractSession(info)
        dbRecord = session.query(RoleModelEx).filter_by(id=id).one()
    except Exception as e:
        print('An error occured (by_id)')
        print(e)
    print(f'to_dict(dbRecord)')
    return dbRecord
def resolve_roles_name_starts_with(root, info, name):
    try:
        session = extractSession(info)
        dbRecords = session.query(RoleModelEx).filter(RoleModel.name.startswith(name)).all()
    except Exception as e:
        print('An error occured (startswith)')
        print(e)
    return dbRecords
def resolve_roles_lastchange_starts_with(root, info, lastchange):
    try:
        session = extractSession(info)
        dbRecords = session.query(RoleModelEx).filter(RoleModel.lastchange.startswith(lastchange)).all()
    except Exception as e:
        print('An error occured (startswith)')
        print(e)
    return dbRecords
def resolve_roles_roletype_id_starts_with(root, info, roletype_id):
    try:
        session = extractSession(info)
        dbRecords = session.query(RoleModelEx).filter(RoleModel.roletype_id.startswith(roletype_id)).all()
    except Exception as e:
        print('An error occured (startswith)')
        print(e)
    return dbRecords
def resolve_roles_user_id_starts_with(root, info, user_id):
    try:
        session = extractSession(info)
        dbRecords = session.query(RoleModelEx).filter(RoleModel.user_id.startswith(user_id)).all()
    except Exception as e:
        print('An error occured (startswith)')
        print(e)
    return dbRecords
def resolve_roles_group_id_starts_with(root, info, group_id):
    try:
        session = extractSession(info)
        dbRecords = session.query(RoleModelEx).filter(RoleModel.group_id.startswith(group_id)).all()
    except Exception as e:
        print('An error occured (startswith)')
        print(e)
    return dbRecords