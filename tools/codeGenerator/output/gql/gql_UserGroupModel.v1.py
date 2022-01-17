import graphene
from sqlalchemy.orm import relationship
from BaseModel import BaseModel

def extractSession(info):
    #return info.context['request'].scope['db_session']
    assert not info.context is None, 'Got Bad Context'
    return info.context.get('session')

class UserGroupModelEx(BaseModel):
    __tablename__ = 'users_groups'
    __table_args__ = {'extend_existing': True} 
    
    usermodel = relationship('UserModelEx')
    # usermodel = association_proxy('usermodel', 'keyword')
    groupmodel = relationship('GroupModelEx')
    # groupmodel = association_proxy('groupmodel', 'keyword')


class UserGroupModel(graphene.ObjectType):
    
    id = graphene.String()
    user_id = graphene.String()
    group_id = graphene.String()
    
        
    usermodel = graphene.Field('graphqltypes.gql_UserModel.UserModel')
    def resolver_usermodel(parent, info):
        return parent.usermodel
        
    groupmodel = graphene.Field('graphqltypes.gql_GroupModel.GroupModel')
    def resolver_groupmodel(parent, info):
        return parent.groupmodel


class create_UserGroupModel(graphene.Mutation):
    class Arguments:
        id = graphene.String(required=True)
        user_id = graphene.String(required=True)
        group_id = graphene.String(required=True)

    ok = graphene.Boolean()
    result = graphene.Field('graphqltypes.gql_UserGroupModel.UserGroupModel')
    
    def mutate(parent, info, **paramList):
        session = extractSession(info)
        result = UserGroupModelEx(**paramList)
        session.add(result)
        session.commit()
        return create_UserGroupModel(ok=True, result=result)
    pass

class update_UserGroupModel(graphene.Mutation):
    class Arguments:
        id = graphene.String(required=True)    
        user_id = graphene.String(required=False)    
        group_id = graphene.String(required=False)

    ok = graphene.Boolean()
    result = graphene.Field('graphqltypes.gql_UserGroupModel.UserGroupModel')
    
    def mutate(parent, info, **paramList):
        session = extractSession(info)
        dbRecord = session.query(UserGroupModelEx).filter_by(id=paramList['id']).one()
        for key, item in paramList.items():
            if key=='id':
                continue
            setattr(dbRecord, key, item)
        session.commit()
        return update_UserGroupModel(ok=True, result=dbRecord)
    pass

def to_dict(row):
    return {column.name: getattr(row, row.__mapper__.get_property_by_column(column).key) for column in row.__table__.columns}


def resolve_users_groups_by_id(root, info, id):
    try:
        session = extractSession(info)
        dbRecord = session.query(UserGroupModelEx).filter_by(id=id).one()
    except Exception as e:
        print('An error occured (by_id)')
        print(e)
    print(f'to_dict(dbRecord)')
    return dbRecord
def resolve_users_groups_user_id_starts_with(root, info, user_id):
    try:
        session = extractSession(info)
        dbRecords = session.query(UserGroupModelEx).filter(UserGroupModel.user_id.startswith(user_id)).all()
    except Exception as e:
        print('An error occured (startswith)')
        print(e)
    return dbRecords
def resolve_users_groups_group_id_starts_with(root, info, group_id):
    try:
        session = extractSession(info)
        dbRecords = session.query(UserGroupModelEx).filter(UserGroupModel.group_id.startswith(group_id)).all()
    except Exception as e:
        print('An error occured (startswith)')
        print(e)
    return dbRecords