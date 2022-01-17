import graphene
from sqlalchemy.orm import relationship
from BaseModel import BaseModel

def extractSession(info):
    #return info.context['request'].scope['db_session']
    assert not info.context is None, 'Got Bad Context'
    return info.context.get('session')

class GroupConnectionModelEx(BaseModel):
    __tablename__ = 'groups_groups'
    __table_args__ = {'extend_existing': True} 
    
    #groupmodel = relationship('GroupModelEx')#, foreign_keys='[GroupModelEx.id]')
    # groupmodel = association_proxy('groupmodel', 'keyword')


class GroupConnectionModel(graphene.ObjectType):
    
    id = graphene.String()
    child_id = graphene.String()
    parent_id = graphene.String()
    
        
    groupmodel = graphene.Field('graphqltypes.gql_GroupModel.GroupModel')
    def resolver_groupmodel(parent, info):
        return parent.groupmodel


class create_GroupConnectionModel(graphene.Mutation):
    class Arguments:
        id = graphene.String(required=True)
        child_id = graphene.String(required=True)
        parent_id = graphene.String(required=True)

    ok = graphene.Boolean()
    result = graphene.Field('graphqltypes.gql_GroupConnectionModel.GroupConnectionModel')
    
    def mutate(parent, info, **paramList):
        session = extractSession(info)
        result = GroupConnectionModelEx(**paramList)
        session.add(result)
        session.commit()
        return create_GroupConnectionModel(ok=True, result=result)
    pass

class update_GroupConnectionModel(graphene.Mutation):
    class Arguments:
        id = graphene.String(required=True)    
        child_id = graphene.String(required=False)    
        parent_id = graphene.String(required=False)

    ok = graphene.Boolean()
    result = graphene.Field('graphqltypes.gql_GroupConnectionModel.GroupConnectionModel')
    
    def mutate(parent, info, **paramList):
        session = extractSession(info)
        dbRecord = session.query(GroupConnectionModelEx).filter_by(id=paramList['id']).one()
        for key, item in paramList.items():
            if key=='id':
                continue
            setattr(dbRecord, key, item)
        session.commit()
        return update_GroupConnectionModel(ok=True, result=dbRecord)
    pass

def to_dict(row):
    return {column.name: getattr(row, row.__mapper__.get_property_by_column(column).key) for column in row.__table__.columns}


def resolve_groups_groups_by_id(root, info, id):
    try:
        session = extractSession(info)
        dbRecord = session.query(GroupConnectionModelEx).filter_by(id=id).one()
    except Exception as e:
        print('An error occured (by_id)')
        print(e)
    print(f'to_dict(dbRecord)')
    return dbRecord
def resolve_groups_groups_child_id_starts_with(root, info, child_id):
    try:
        session = extractSession(info)
        dbRecords = session.query(GroupConnectionModelEx).filter(GroupConnectionModel.child_id.startswith(child_id)).all()
    except Exception as e:
        print('An error occured (startswith)')
        print(e)
    return dbRecords
def resolve_groups_groups_parent_id_starts_with(root, info, parent_id):
    try:
        session = extractSession(info)
        dbRecords = session.query(GroupConnectionModelEx).filter(GroupConnectionModel.parent_id.startswith(parent_id)).all()
    except Exception as e:
        print('An error occured (startswith)')
        print(e)
    return dbRecords