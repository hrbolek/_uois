import graphene
from sqlalchemy.orm import relationship
from BaseModel import BaseModel

def extractSession(info):
    #return info.context['request'].scope['db_session']
    assert not info.context is None, 'Got Bad Context'
    return info.context.get('session')

class GroupTypeModel(BaseModel):
    __tablename__ = 'grouptypes'
    __table_args__ = {'extend_existing': True} 
    
    groupmodel_collection = relationship('GroupModel')
    # groupmodel_collection = association_proxy('groupmodel_collection', 'keyword')


class get_GroupTypeModel(graphene.ObjectType):
    
    id = graphene.String()
    name = graphene.String()
    
        
    groupmodel_collection = graphene.List('gql_GroupModel.get_GroupModel')
        
    def resolver_groupmodel_collection(parent, info):
        return parent.groupmodel_collection


class create_GroupTypeModel(graphene.Mutation):
    class Arguments:
        id = graphene.String(required=True)
        name = graphene.String(required=True)

    ok = graphene.Boolean()
    result = graphene.Field('get_GroupTypeModel')
    
    def mutate(parent, info, **paramList):
        session = extractSession(info)
        result = GroupTypeModel(**paramList)
        session.add(result)
        session.commit()
        return create_GroupTypeModel(ok=True, result=result)
    pass

class update_GroupTypeModel(graphene.Mutation):
    class Arguments:
        id = graphene.String(required=True)    
        name = graphene.String(required=False)

    ok = graphene.Boolean()
    result = graphene.Field('get_GroupTypeModel')
    
    def mutate(parent, info, **paramList):
        session = extractSession(info)
        dbRecord = session.query(GroupTypeModel).filter_by(id=paramList['id']).one()
        for key, item in paramList.items():
            if key=='id':
                continue
            setattr(dbRecord, key, item)
        session.commit()
        return update_GroupTypeModel(ok=True, result=dbRecord)
    pass


def resolve_grouptypes_by_id(root, info, id):
    session = extractSession(info)
    dbRecord = session.query(GroupTypeModel).filter_by(id=id).one()
    return dbRecord
def resolve_grouptypes_name_starts_with(root, info, name):
    session = extractSession(info)
    dbRecords = session.query(GroupTypeModel).filter(GroupTypeModel.name.startswith(name)).all()
    return dbRecords