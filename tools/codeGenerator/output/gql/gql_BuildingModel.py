import graphene
from sqlalchemy.orm import relationship
from BaseModel import BaseModel

def extractSession(info):
    #return info.context['request'].scope['db_session']
    assert not info.context is None, 'Got Bad Context'
    return info.context.get('session')

class BuildingModel(BaseModel):
    __tablename__ = 'buildings'
    __table_args__ = {'extend_existing': True} 
    
    arealmodel = relationship('ArealModel')
    # arealmodel = association_proxy('arealmodel', 'keyword')
    roommodel_collection = relationship('RoomModel')
    # roommodel_collection = association_proxy('roommodel_collection', 'keyword')


class get_BuildingModel(graphene.ObjectType):
    
    id = graphene.String()
    name = graphene.String()
    lastchange = graphene.DateTime()
    externalId = graphene.String()
    areal_id = graphene.String()
    
        
    arealmodel = graphene.Field('gql_ArealModel.get_ArealModel')
    def resolver_arealmodel(parent, info):
        return parent.arealmodel
        
    roommodel_collection = graphene.List('gql_RoomModel.get_RoomModel')
        
    def resolver_roommodel_collection(parent, info):
        return parent.roommodel_collection


class create_BuildingModel(graphene.Mutation):
    class Arguments:
        id = graphene.String(required=True)
        name = graphene.String(required=True)
        lastchange = graphene.DateTime(required=True)
        externalId = graphene.String(required=True)
        areal_id = graphene.String(required=True)

    ok = graphene.Boolean()
    result = graphene.Field('get_BuildingModel')
    
    def mutate(parent, info, **paramList):
        session = extractSession(info)
        result = BuildingModel(**paramList)
        session.add(result)
        session.commit()
        return create_BuildingModel(ok=True, result=result)
    pass

class update_BuildingModel(graphene.Mutation):
    class Arguments:
        id = graphene.String(required=True)    
        name = graphene.String(required=False)    
        lastchange = graphene.DateTime(required=False)    
        externalId = graphene.String(required=False)    
        areal_id = graphene.String(required=False)

    ok = graphene.Boolean()
    result = graphene.Field('get_BuildingModel')
    
    def mutate(parent, info, **paramList):
        session = extractSession(info)
        dbRecord = session.query(BuildingModel).filter_by(id=paramList['id']).one()
        for key, item in paramList.items():
            if key=='id':
                continue
            setattr(dbRecord, key, item)
        session.commit()
        return update_BuildingModel(ok=True, result=dbRecord)
    pass


def resolve_buildings_by_id(root, info, id):
    session = extractSession(info)
    dbRecord = session.query(BuildingModel).filter_by(id=id).one()
    return dbRecord
def resolve_buildings_name_starts_with(root, info, name):
    session = extractSession(info)
    dbRecords = session.query(BuildingModel).filter(BuildingModel.name.startswith(name)).all()
    return dbRecords
def resolve_buildings_lastchange_starts_with(root, info, lastchange):
    session = extractSession(info)
    dbRecords = session.query(BuildingModel).filter(BuildingModel.lastchange.startswith(lastchange)).all()
    return dbRecords
def resolve_buildings_externalId_starts_with(root, info, externalId):
    session = extractSession(info)
    dbRecords = session.query(BuildingModel).filter(BuildingModel.externalId.startswith(externalId)).all()
    return dbRecords
def resolve_buildings_areal_id_starts_with(root, info, areal_id):
    session = extractSession(info)
    dbRecords = session.query(BuildingModel).filter(BuildingModel.areal_id.startswith(areal_id)).all()
    return dbRecords