import graphene
from sqlalchemy.orm import relationship
from BaseModel import BaseModel

def extractSession(info):
    #return info.context['request'].scope['db_session']
    assert not info.context is None, 'Got Bad Context'
    return info.context.get('session')

class RoleTypeModelEx(BaseModel):
    __tablename__ = 'grouproletypes'
    __table_args__ = {'extend_existing': True} 
    
    rolemodels = relationship('RoleModelEx')
    # rolemodels = association_proxy('rolemodels', 'keyword')


class RoleTypeModel(graphene.ObjectType):
    
    id = graphene.String()
    name = graphene.String()
    
        
    rolemodels = graphene.List('graphqltypes.gql_RoleModel.RoleModel')
        
    def resolver_rolemodels(parent, info):
        return parent.rolemodels


class create_RoleTypeModel(graphene.Mutation):
    class Arguments:
        id = graphene.String(required=True)
        name = graphene.String(required=True)

    ok = graphene.Boolean()
    result = graphene.Field('graphqltypes.gql_RoleTypeModel.RoleTypeModel')
    
    def mutate(parent, info, **paramList):
        session = extractSession(info)
        result = RoleTypeModelEx(**paramList)
        session.add(result)
        session.commit()
        return create_RoleTypeModel(ok=True, result=result)
    pass

class update_RoleTypeModel(graphene.Mutation):
    class Arguments:
        id = graphene.String(required=True)    
        name = graphene.String(required=False)

    ok = graphene.Boolean()
    result = graphene.Field('graphqltypes.gql_RoleTypeModel.RoleTypeModel')
    
    def mutate(parent, info, **paramList):
        session = extractSession(info)
        dbRecord = session.query(RoleTypeModelEx).filter_by(id=paramList['id']).one()
        for key, item in paramList.items():
            if key=='id':
                continue
            setattr(dbRecord, key, item)
        session.commit()
        return update_RoleTypeModel(ok=True, result=dbRecord)
    pass

def to_dict(row):
    return {column.name: getattr(row, row.__mapper__.get_property_by_column(column).key) for column in row.__table__.columns}


def resolve_grouproletypes_by_id(root, info, id):
    try:
        session = extractSession(info)
        dbRecord = session.query(RoleTypeModelEx).filter_by(id=id).one()
    except Exception as e:
        print('An error occured (by_id)')
        print(e)
    print(f'to_dict(dbRecord)')
    return dbRecord
def resolve_grouproletypes_name_starts_with(root, info, name):
    try:
        session = extractSession(info)
        dbRecords = session.query(RoleTypeModelEx).filter(RoleTypeModel.name.startswith(name)).all()
    except Exception as e:
        print('An error occured (startswith)')
        print(e)
    return dbRecords