import graphene
from sqlalchemy.orm import relationship
from BaseModel import BaseModel

def extractSession(info):
    #return info.context['request'].scope['db_session']
    assert not info.context is None, 'Got Bad Context'
    return info.context.get('session')

class EventModel(BaseModel):
    __tablename__ = 'events'
    __table_args__ = {'extend_existing': True} 
    
    eventusermodel_collection = relationship('EventUserModel')
    # eventusermodel_collection = association_proxy('eventusermodel_collection', 'keyword')
    eventgroupmodel_collection = relationship('EventGroupModel')
    # eventgroupmodel_collection = association_proxy('eventgroupmodel_collection', 'keyword')
    studyplanitemeventmodel_collection = relationship('StudyPlanItemEventModel')
    # studyplanitemeventmodel_collection = association_proxy('studyplanitemeventmodel_collection', 'keyword')
    eventroommodel_collection = relationship('EventRoomModel')
    # eventroommodel_collection = association_proxy('eventroommodel_collection', 'keyword')


class get_EventModel(graphene.ObjectType):
    
    id = graphene.String()
    start = graphene.DateTime()
    end = graphene.DateTime()
    label = graphene.String()
    externalId = graphene.String()
    lastchange = graphene.DateTime()
    
        
    eventusermodel_collection = graphene.List('gql_EventUserModel.get_EventUserModel')
        
    def resolver_eventusermodel_collection(parent, info):
        return parent.eventusermodel_collection
        
    eventgroupmodel_collection = graphene.List('gql_EventGroupModel.get_EventGroupModel')
        
    def resolver_eventgroupmodel_collection(parent, info):
        return parent.eventgroupmodel_collection
        
    studyplanitemeventmodel_collection = graphene.List('gql_StudyPlanItemEventModel.get_StudyPlanItemEventModel')
        
    def resolver_studyplanitemeventmodel_collection(parent, info):
        return parent.studyplanitemeventmodel_collection
        
    eventroommodel_collection = graphene.List('gql_EventRoomModel.get_EventRoomModel')
        
    def resolver_eventroommodel_collection(parent, info):
        return parent.eventroommodel_collection


class create_EventModel(graphene.Mutation):
    class Arguments:
        id = graphene.String(required=True)
        start = graphene.DateTime(required=True)
        end = graphene.DateTime(required=True)
        label = graphene.String(required=True)
        externalId = graphene.String(required=True)
        lastchange = graphene.DateTime(required=True)

    ok = graphene.Boolean()
    result = graphene.Field('get_EventModel')
    
    def mutate(parent, info, **paramList):
        session = extractSession(info)
        result = EventModel(**paramList)
        session.add(result)
        session.commit()
        return create_EventModel(ok=True, result=result)
    pass

class update_EventModel(graphene.Mutation):
    class Arguments:
        id = graphene.String(required=True)    
        start = graphene.DateTime(required=False)    
        end = graphene.DateTime(required=False)    
        label = graphene.String(required=False)    
        externalId = graphene.String(required=False)    
        lastchange = graphene.DateTime(required=False)

    ok = graphene.Boolean()
    result = graphene.Field('get_EventModel')
    
    def mutate(parent, info, **paramList):
        session = extractSession(info)
        dbRecord = session.query(EventModel).filter_by(id=paramList['id']).one()
        for key, item in paramList.items():
            if key=='id':
                continue
            setattr(dbRecord, key, item)
        session.commit()
        return update_EventModel(ok=True, result=dbRecord)
    pass


def resolve_events_by_id(root, info, id):
    session = extractSession(info)
    dbRecord = session.query(EventModel).filter_by(id=id).one()
    return dbRecord
def resolve_events_start_starts_with(root, info, start):
    session = extractSession(info)
    dbRecords = session.query(EventModel).filter(EventModel.start.startswith(start)).all()
    return dbRecords
def resolve_events_end_starts_with(root, info, end):
    session = extractSession(info)
    dbRecords = session.query(EventModel).filter(EventModel.end.startswith(end)).all()
    return dbRecords
def resolve_events_label_starts_with(root, info, label):
    session = extractSession(info)
    dbRecords = session.query(EventModel).filter(EventModel.label.startswith(label)).all()
    return dbRecords
def resolve_events_externalId_starts_with(root, info, externalId):
    session = extractSession(info)
    dbRecords = session.query(EventModel).filter(EventModel.externalId.startswith(externalId)).all()
    return dbRecords
def resolve_events_lastchange_starts_with(root, info, lastchange):
    session = extractSession(info)
    dbRecords = session.query(EventModel).filter(EventModel.lastchange.startswith(lastchange)).all()
    return dbRecords