import graphene
from sqlalchemy.orm import relationship
from BaseModel import BaseModel

def extractSession(info):
    #return info.context['request'].scope['db_session']
    assert not info.context is None, 'Got Bad Context'
    return info.context.get('session')

class EventRoomModel(BaseModel):
    __tablename__ = 'events_rooms'
    __table_args__ = {'extend_existing': True} 
    
    roommodel = relationship('RoomModel')
    # roommodel = association_proxy('roommodel', 'keyword')
    eventmodel = relationship('EventModel')
    # eventmodel = association_proxy('eventmodel', 'keyword')


class get_EventRoomModel(graphene.ObjectType):
    
    id = graphene.String()
    room_id = graphene.String()
    event_id = graphene.String()
    
        
    roommodel = graphene.Field('gql_RoomModel.get_RoomModel')
    def resolver_roommodel(parent, info):
        return parent.roommodel
        
    eventmodel = graphene.Field('gql_EventModel.get_EventModel')
    def resolver_eventmodel(parent, info):
        return parent.eventmodel


class create_EventRoomModel(graphene.Mutation):
    class Arguments:
        id = graphene.String(required=True)
        room_id = graphene.String(required=True)
        event_id = graphene.String(required=True)

    ok = graphene.Boolean()
    result = graphene.Field('get_EventRoomModel')
    
    def mutate(parent, info, **paramList):
        session = extractSession(info)
        result = EventRoomModel(**paramList)
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
    result = graphene.Field('get_EventRoomModel')
    
    def mutate(parent, info, **paramList):
        session = extractSession(info)
        dbRecord = session.query(EventRoomModel).filter_by(id=paramList['id']).one()
        for key, item in paramList.items():
            if key=='id':
                continue
            setattr(dbRecord, key, item)
        session.commit()
        return update_EventRoomModel(ok=True, result=dbRecord)
    pass


def resolve_events_rooms_by_id(root, info, id):
    session = extractSession(info)
    dbRecord = session.query(EventRoomModel).filter_by(id=id).one()
    return dbRecord
def resolve_events_rooms_room_id_starts_with(root, info, room_id):
    session = extractSession(info)
    dbRecords = session.query(EventRoomModel).filter(EventRoomModel.room_id.startswith(room_id)).all()
    return dbRecords
def resolve_events_rooms_event_id_starts_with(root, info, event_id):
    session = extractSession(info)
    dbRecords = session.query(EventRoomModel).filter(EventRoomModel.event_id.startswith(event_id)).all()
    return dbRecords