import graphene
from sqlalchemy.orm import relationship
from BaseModel import BaseModel

def extractSession(info):
    #return info.context['request'].scope['db_session']
    assert not info.context is None, 'Got Bad Context'
    return info.context.get('session')

class RoomModel(BaseModel):
    __tablename__ = 'rooms'
    __table_args__ = {'extend_existing': True} 
    
    buildingmodel = relationship('BuildingModel')
    # buildingmodel = association_proxy('buildingmodel', 'keyword')
    eventroommodel_collection = relationship('EventRoomModel')
    # eventroommodel_collection = association_proxy('eventroommodel_collection', 'keyword')


class get_RoomModel(graphene.ObjectType):
    
    id = graphene.String()
    name = graphene.String()
    lastchange = graphene.DateTime()
    externalId = graphene.String()
    building_id = graphene.String()
    
        
    buildingmodel = graphene.Field('gql_BuildingModel.get_BuildingModel')
    def resolver_buildingmodel(parent, info):
        return parent.buildingmodel
        
    eventroommodel_collection = graphene.List('gql_EventRoomModel.get_EventRoomModel')
        
    def resolver_eventroommodel_collection(parent, info):
        return parent.eventroommodel_collection


class create_RoomModel(graphene.Mutation):
    class Arguments:
        id = graphene.String(required=True)
        name = graphene.String(required=True)
        lastchange = graphene.DateTime(required=True)
        externalId = graphene.String(required=True)
        building_id = graphene.String(required=True)

    ok = graphene.Boolean()
    result = graphene.Field('get_RoomModel')
    
    def mutate(parent, info, **paramList):
        session = extractSession(info)
        result = RoomModel(**paramList)
        session.add(result)
        session.commit()
        return create_RoomModel(ok=True, result=result)
    pass

class update_RoomModel(graphene.Mutation):
    class Arguments:
        id = graphene.String(required=True)    
        name = graphene.String(required=False)    
        lastchange = graphene.DateTime(required=False)    
        externalId = graphene.String(required=False)    
        building_id = graphene.String(required=False)

    ok = graphene.Boolean()
    result = graphene.Field('get_RoomModel')
    
    def mutate(parent, info, **paramList):
        session = extractSession(info)
        dbRecord = session.query(RoomModel).filter_by(id=paramList['id']).one()
        for key, item in paramList.items():
            if key=='id':
                continue
            setattr(dbRecord, key, item)
        session.commit()
        return update_RoomModel(ok=True, result=dbRecord)
    pass


def resolve_rooms_by_id(root, info, id):
    session = extractSession(info)
    dbRecord = session.query(RoomModel).filter_by(id=id).one()
    return dbRecord
def resolve_rooms_name_starts_with(root, info, name):
    session = extractSession(info)
    dbRecords = session.query(RoomModel).filter(RoomModel.name.startswith(name)).all()
    return dbRecords
def resolve_rooms_lastchange_starts_with(root, info, lastchange):
    session = extractSession(info)
    dbRecords = session.query(RoomModel).filter(RoomModel.lastchange.startswith(lastchange)).all()
    return dbRecords
def resolve_rooms_externalId_starts_with(root, info, externalId):
    session = extractSession(info)
    dbRecords = session.query(RoomModel).filter(RoomModel.externalId.startswith(externalId)).all()
    return dbRecords
def resolve_rooms_building_id_starts_with(root, info, building_id):
    session = extractSession(info)
    dbRecords = session.query(RoomModel).filter(RoomModel.building_id.startswith(building_id)).all()
    return dbRecords