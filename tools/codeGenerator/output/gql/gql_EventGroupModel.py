import graphene
from sqlalchemy.orm import relationship
from BaseModel import BaseModel

def extractSession(info):
    #return info.context['request'].scope['db_session']
    assert not info.context is None, 'Got Bad Context'
    return info.context.get('session')

class EventGroupModel(BaseModel):
    __tablename__ = 'events_groups'
    __table_args__ = {'extend_existing': True} 
    
    eventmodel = relationship('EventModel')
    # eventmodel = association_proxy('eventmodel', 'keyword')
    groupmodel = relationship('GroupModel')
    # groupmodel = association_proxy('groupmodel', 'keyword')


class get_EventGroupModel(graphene.ObjectType):
    
    id = graphene.String()
    group_id = graphene.String()
    event_id = graphene.String()
    
        
    eventmodel = graphene.Field('gql_EventModel.get_EventModel')
    def resolver_eventmodel(parent, info):
        return parent.eventmodel
        
    groupmodel = graphene.Field('gql_GroupModel.get_GroupModel')
    def resolver_groupmodel(parent, info):
        return parent.groupmodel


class create_EventGroupModel(graphene.Mutation):
    class Arguments:
        id = graphene.String(required=True)
        group_id = graphene.String(required=True)
        event_id = graphene.String(required=True)

    ok = graphene.Boolean()
    result = graphene.Field('get_EventGroupModel')
    
    def mutate(parent, info, **paramList):
        session = extractSession(info)
        result = EventGroupModel(**paramList)
        session.add(result)
        session.commit()
        return create_EventGroupModel(ok=True, result=result)
    pass

class update_EventGroupModel(graphene.Mutation):
    class Arguments:
        id = graphene.String(required=True)    
        group_id = graphene.String(required=False)    
        event_id = graphene.String(required=False)

    ok = graphene.Boolean()
    result = graphene.Field('get_EventGroupModel')
    
    def mutate(parent, info, **paramList):
        session = extractSession(info)
        dbRecord = session.query(EventGroupModel).filter_by(id=paramList['id']).one()
        for key, item in paramList.items():
            if key=='id':
                continue
            setattr(dbRecord, key, item)
        session.commit()
        return update_EventGroupModel(ok=True, result=dbRecord)
    pass


def resolve_events_groups_by_id(root, info, id):
    session = extractSession(info)
    dbRecord = session.query(EventGroupModel).filter_by(id=id).one()
    return dbRecord
def resolve_events_groups_group_id_starts_with(root, info, group_id):
    session = extractSession(info)
    dbRecords = session.query(EventGroupModel).filter(EventGroupModel.group_id.startswith(group_id)).all()
    return dbRecords
def resolve_events_groups_event_id_starts_with(root, info, event_id):
    session = extractSession(info)
    dbRecords = session.query(EventGroupModel).filter(EventGroupModel.event_id.startswith(event_id)).all()
    return dbRecords