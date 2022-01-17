import graphene
from sqlalchemy.orm import relationship
from BaseModel import BaseModel

def extractSession(info):
    #return info.context['request'].scope['db_session']
    assert not info.context is None, 'Got Bad Context'
    return info.context.get('session')

class EventRoomModelEx(BaseModel):
    __tablename__ = 'events_rooms'
    __table_args__ = {'extend_existing': True} 
    
    roommodel = relationship('RoomModelEx')
    # roommodel = association_proxy('roommodel', 'keyword')
    eventmodel = relationship('EventModelEx')
    # eventmodel = association_proxy('eventmodel', 'keyword')


class EventRoomModel(graphene.ObjectType):
    
    id = graphene.String()
    room_id = graphene.String()
    event_id = graphene.String()
    
        
    roommodel = graphene.Field('graphqltypes.gql_RoomModel.RoomModel')
    def resolver_roommodel(parent, info):
        return parent.roommodel
        
    eventmodel = graphene.Field('graphqltypes.gql_EventModel.EventModel')
    def resolver_eventmodel(parent, info):
        return parent.eventmodel


class create_EventRoomModel(graphene.Mutation):
    class Arguments:
        id = graphene.String(required=True)
        room_id = graphene.String(required=True)
        event_id = graphene.String(required=True)

    ok = graphene.Boolean()
    result = graphene.Field('graphqltypes.gql_EventRoomModel.EventRoomModel')
    
    def mutate(parent, info, **paramList):
        session = extractSession(info)
        result = EventRoomModelEx(**paramList)
        session.add(result)
        session.commit()
        return create_EventRoomModel(ok=True, result=result)
    pass

class update_EventRoomModel(graphene.Mutation):
    class Arguments:
        id = graphene.String(required=True)    
        room_id = graphene.String(required=False)    
        event_id = graphene.String(required=False)

    ok = graphene.Boolean()
    result = graphene.Field('graphqltypes.gql_EventRoomModel.EventRoomModel')
    
    def mutate(parent, info, **paramList):
        session = extractSession(info)
        dbRecord = session.query(EventRoomModelEx).filter_by(id=paramList['id']).one()
        for key, item in paramList.items():
            if key=='id':
                continue
            setattr(dbRecord, key, item)
        session.commit()
        return update_EventRoomModel(ok=True, result=dbRecord)
    pass

def to_dict(row):
    return {column.name: getattr(row, row.__mapper__.get_property_by_column(column).key) for column in row.__table__.columns}


def resolve_events_rooms_by_id(root, info, id):
    try:
        session = extractSession(info)
        dbRecord = session.query(EventRoomModelEx).filter_by(id=id).one()
    except Exception as e:
        print('An error occured (by_id)')
        print(e)
    print(f'to_dict(dbRecord)')
    return dbRecord
def resolve_events_rooms_room_id_starts_with(root, info, room_id):
    try:
        session = extractSession(info)
        dbRecords = session.query(EventRoomModelEx).filter(EventRoomModel.room_id.startswith(room_id)).all()
    except Exception as e:
        print('An error occured (startswith)')
        print(e)
    return dbRecords
def resolve_events_rooms_event_id_starts_with(root, info, event_id):
    try:
        session = extractSession(info)
        dbRecords = session.query(EventRoomModelEx).filter(EventRoomModel.event_id.startswith(event_id)).all()
    except Exception as e:
        print('An error occured (startswith)')
        print(e)
    return dbRecords