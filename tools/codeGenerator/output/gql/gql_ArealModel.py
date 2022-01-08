import graphene
from sqlalchemy.orm import relationship
from BaseModel import BaseModel

def extractSession(info):
    #return info.context['request'].scope['db_session']
    assert not info.context is None, 'Got Bad Context'
    return info.context.get('session')

class ArealModel(BaseModel):
    __tablename__ = 'areals'
    __table_args__ = {'extend_existing': True} 
    
    buildingmodel_collection = relationship('BuildingModel')
    # buildingmodel_collection = association_proxy('buildingmodel_collection', 'keyword')


class get_ArealModel(graphene.ObjectType):
    
    id = graphene.String()
    name = graphene.String()
    externalId = graphene.String()
    lastchange = graphene.DateTime()
    
        
    buildingmodel_collection = graphene.List('gql_BuildingModel.get_BuildingModel')
        
    def resolver_buildingmodel_collection(parent, info):
        return parent.buildingmodel_collection


class create_ArealModel(graphene.Mutation):
    class Arguments:
        id = graphene.String(required=True)
        name = graphene.String(required=True)
        externalId = graphene.String(required=True)
        lastchange = graphene.DateTime(required=True)

    ok = graphene.Boolean()
    result = graphene.Field('get_ArealModel')
    
    def mutate(parent, info, **paramList):
        session = extractSession(info)
        result = ArealModel(**paramList)
        session.add(result)
        session.commit()
        return create_ArealModel(ok=True, result=result)
    pass

class update_ArealModel(graphene.Mutation):
    class Arguments:
        id = graphene.String(required=True)    
        name = graphene.String(required=False)    
        externalId = graphene.String(required=False)    
        lastchange = graphene.DateTime(required=False)

    ok = graphene.Boolean()
    result = graphene.Field('get_ArealModel')
    
    def mutate(parent, info, **paramList):
        session = extractSession(info)
        dbRecord = session.query(ArealModel).filter_by(id=paramList['id']).one()
        for key, item in paramList.items():
            if key=='id':
                continue
            setattr(dbRecord, key, item)
        session.commit()
        return update_ArealModel(ok=True, result=dbRecord)
    pass


def resolve_areals_by_id(root, info, id):
    session = extractSession(info)
    dbRecord = session.query(ArealModel).filter_by(id=id).one()
    return dbRecord
def resolve_areals_name_starts_with(root, info, name):
    session = extractSession(info)
    dbRecords = session.query(ArealModel).filter(ArealModel.name.startswith(name)).all()
    return dbRecords
def resolve_areals_externalId_starts_with(root, info, externalId):
    session = extractSession(info)
    dbRecords = session.query(ArealModel).filter(ArealModel.externalId.startswith(externalId)).all()
    return dbRecords
def resolve_areals_lastchange_starts_with(root, info, lastchange):
    session = extractSession(info)
    dbRecords = session.query(ArealModel).filter(ArealModel.lastchange.startswith(lastchange)).all()
    return dbRecords