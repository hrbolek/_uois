import graphene
from sqlalchemy.orm import relationship
from BaseModel import BaseModel

def extractSession(info):
    #return info.context['request'].scope['db_session']
    assert not info.context is None, 'Got Bad Context'
    return info.context.get('session')

class RoleTypeModel(BaseModel):
    __tablename__ = 'grouproletypes'
    __table_args__ = {'extend_existing': True} 
    
    rolemodel_collection = relationship('RoleModel')
    # rolemodel_collection = association_proxy('rolemodel_collection', 'keyword')


class get_RoleTypeModel(graphene.ObjectType):
    
    id = graphene.String()
    name = graphene.String()
    
        
    rolemodel_collection = graphene.List('gql_RoleModel.get_RoleModel')
        
    def resolver_rolemodel_collection(parent, info):
        return parent.rolemodel_collection


class create_RoleTypeModel(graphene.Mutation):
    class Arguments:
        id = graphene.String(required=True)
        name = graphene.String(required=True)

    ok = graphene.Boolean()
    result = graphene.Field('get_RoleTypeModel')
    
    def mutate(parent, info, **paramList):
        session = extractSession(info)
        result = RoleTypeModel(**paramList)
        session.add(result)
        session.commit()
        return create_RoleTypeModel(ok=True, result=result)
    pass

class update_RoleTypeModel(graphene.Mutation):
    class Arguments:
        id = graphene.String(required=True)    
        name = graphene.String(required=False)

    ok = graphene.Boolean()
    result = graphene.Field('get_RoleTypeModel')
    
    def mutate(parent, info, **paramList):
        session = extractSession(info)
        dbRecord = session.query(RoleTypeModel).filter_by(id=paramList['id']).one()
        for key, item in paramList.items():
            if key=='id':
                continue
            setattr(dbRecord, key, item)
        session.commit()
        return update_RoleTypeModel(ok=True, result=dbRecord)
    pass


def resolve_grouproletypes_by_id(root, info, id):
    session = extractSession(info)
    dbRecord = session.query(RoleTypeModel).filter_by(id=id).one()
    return dbRecord
def resolve_grouproletypes_name_starts_with(root, info, name):
    session = extractSession(info)
    dbRecords = session.query(RoleTypeModel).filter(RoleTypeModel.name.startswith(name)).all()
    return dbRecords