import graphene
from sqlalchemy.orm import relationship
from BaseModel import BaseModel

def extractSession(info):
    #return info.context['request'].scope['db_session']
    assert not info.context is None, 'Got Bad Context'
    return info.context.get('session')

class RoomModelEx(BaseModel):
    __tablename__ = 'rooms'
    __table_args__ = {'extend_existing': True} 
    
    buildingmodel = relationship('BuildingModelEx')
    # buildingmodel = association_proxy('buildingmodel', 'keyword')
    eventroommodels = relationship('EventRoomModelEx')
    # eventroommodels = association_proxy('eventroommodels', 'keyword')


class RoomModel(graphene.ObjectType):
    
    id = graphene.String()
    name = graphene.String()
    lastchange = graphene.DateTime()
    externalId = graphene.String()
    building_id = graphene.String()
    
        
    buildingmodel = graphene.Field('graphqltypes.gql_BuildingModel.BuildingModel')
    def resolver_buildingmodel(parent, info):
        return parent.buildingmodel
        
    eventroommodels = graphene.List('graphqltypes.gql_EventRoomModel.EventRoomModel')
        
    def resolver_eventroommodels(parent, info):
        return parent.eventroommodels


class create_RoomModel(graphene.Mutation):
    class Arguments:
        id = graphene.String(required=True)
        name = graphene.String(required=True)
        lastchange = graphene.DateTime(required=True)
        externalId = graphene.String(required=True)
        building_id = graphene.String(required=True)

    ok = graphene.Boolean()
    result = graphene.Field('graphqltypes.gql_RoomModel.RoomModel')
    
    def mutate(parent, info, **paramList):
        session = extractSession(info)
        result = RoomModelEx(**paramList)
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
    result = graphene.Field('graphqltypes.gql_RoomModel.RoomModel')
    
    def mutate(parent, info, **paramList):
        session = extractSession(info)
        dbRecord = session.query(RoomModelEx).filter_by(id=paramList['id']).one()
        for key, item in paramList.items():
            if key=='id':
                continue
            setattr(dbRecord, key, item)
        session.commit()
        return update_RoomModel(ok=True, result=dbRecord)
    pass

def to_dict(row):
    return {column.name: getattr(row, row.__mapper__.get_property_by_column(column).key) for column in row.__table__.columns}


def resolve_rooms_by_id(root, info, id):
    try:
        session = extractSession(info)
        dbRecord = session.query(RoomModelEx).filter_by(id=id).one()
    except Exception as e:
        print('An error occured (by_id)')
        print(e)
    print(f'to_dict(dbRecord)')
    return dbRecord
def resolve_rooms_name_starts_with(root, info, name):
    try:
        session = extractSession(info)
        dbRecords = session.query(RoomModelEx).filter(RoomModel.name.startswith(name)).all()
    except Exception as e:
        print('An error occured (startswith)')
        print(e)
    return dbRecords
def resolve_rooms_lastchange_starts_with(root, info, lastchange):
    try:
        session = extractSession(info)
        dbRecords = session.query(RoomModelEx).filter(RoomModel.lastchange.startswith(lastchange)).all()
    except Exception as e:
        print('An error occured (startswith)')
        print(e)
    return dbRecords
def resolve_rooms_externalId_starts_with(root, info, externalId):
    try:
        session = extractSession(info)
        dbRecords = session.query(RoomModelEx).filter(RoomModel.externalId.startswith(externalId)).all()
    except Exception as e:
        print('An error occured (startswith)')
        print(e)
    return dbRecords
def resolve_rooms_building_id_starts_with(root, info, building_id):
    try:
        session = extractSession(info)
        dbRecords = session.query(RoomModelEx).filter(RoomModel.building_id.startswith(building_id)).all()
    except Exception as e:
        print('An error occured (startswith)')
        print(e)
    return dbRecords