import graphene
from sqlalchemy.orm import relationship
from BaseModel import BaseModel

def extractSession(info):
    #return info.context['request'].scope['db_session']
    assert not info.context is None, 'Got Bad Context'
    return info.context.get('session')

class EventModelEx(BaseModel):
    __tablename__ = 'events'
    __table_args__ = {'extend_existing': True} 
    
    eventusermodels = relationship('EventUserModelEx')
    # eventusermodels = association_proxy('eventusermodels', 'keyword')
    eventgroupmodels = relationship('EventGroupModelEx')
    # eventgroupmodels = association_proxy('eventgroupmodels', 'keyword')
    studyplanitemeventmodels = relationship('StudyPlanItemEventModelEx')
    # studyplanitemeventmodels = association_proxy('studyplanitemeventmodels', 'keyword')
    eventroommodels = relationship('EventRoomModelEx')
    # eventroommodels = association_proxy('eventroommodels', 'keyword')


class EventModel(graphene.ObjectType):
    
    id = graphene.String()
    start = graphene.DateTime()
    end = graphene.DateTime()
    label = graphene.String()
    externalId = graphene.String()
    lastchange = graphene.DateTime()
    
        
    eventusermodels = graphene.List('graphqltypes.gql_EventUserModel.EventUserModel')
        
    def resolver_eventusermodels(parent, info):
        return parent.eventusermodels
        
    eventgroupmodels = graphene.List('graphqltypes.gql_EventGroupModel.EventGroupModel')
        
    def resolver_eventgroupmodels(parent, info):
        return parent.eventgroupmodels
        
    studyplanitemeventmodels = graphene.List('graphqltypes.gql_StudyPlanItemEventModel.StudyPlanItemEventModel')
        
    def resolver_studyplanitemeventmodels(parent, info):
        return parent.studyplanitemeventmodels
        
    eventroommodels = graphene.List('graphqltypes.gql_EventRoomModel.EventRoomModel')
        
    def resolver_eventroommodels(parent, info):
        return parent.eventroommodels


class create_EventModel(graphene.Mutation):
    class Arguments:
        id = graphene.String(required=True)
        start = graphene.DateTime(required=True)
        end = graphene.DateTime(required=True)
        label = graphene.String(required=True)
        externalId = graphene.String(required=True)
        lastchange = graphene.DateTime(required=True)

    ok = graphene.Boolean()
    result = graphene.Field('graphqltypes.gql_EventModel.EventModel')
    
    def mutate(parent, info, **paramList):
        session = extractSession(info)
        result = EventModelEx(**paramList)
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
    result = graphene.Field('graphqltypes.gql_EventModel.EventModel')
    
    def mutate(parent, info, **paramList):
        session = extractSession(info)
        dbRecord = session.query(EventModelEx).filter_by(id=paramList['id']).one()
        for key, item in paramList.items():
            if key=='id':
                continue
            setattr(dbRecord, key, item)
        session.commit()
        return update_EventModel(ok=True, result=dbRecord)
    pass

def to_dict(row):
    return {column.name: getattr(row, row.__mapper__.get_property_by_column(column).key) for column in row.__table__.columns}


def resolve_events_by_id(root, info, id):
    try:
        session = extractSession(info)
        dbRecord = session.query(EventModelEx).filter_by(id=id).one()
    except Exception as e:
        print('An error occured (by_id)')
        print(e)
    print(f'to_dict(dbRecord)')
    return dbRecord
def resolve_events_start_starts_with(root, info, start):
    try:
        session = extractSession(info)
        dbRecords = session.query(EventModelEx).filter(EventModel.start.startswith(start)).all()
    except Exception as e:
        print('An error occured (startswith)')
        print(e)
    return dbRecords
def resolve_events_end_starts_with(root, info, end):
    try:
        session = extractSession(info)
        dbRecords = session.query(EventModelEx).filter(EventModel.end.startswith(end)).all()
    except Exception as e:
        print('An error occured (startswith)')
        print(e)
    return dbRecords
def resolve_events_label_starts_with(root, info, label):
    try:
        session = extractSession(info)
        dbRecords = session.query(EventModelEx).filter(EventModel.label.startswith(label)).all()
    except Exception as e:
        print('An error occured (startswith)')
        print(e)
    return dbRecords
def resolve_events_externalId_starts_with(root, info, externalId):
    try:
        session = extractSession(info)
        dbRecords = session.query(EventModelEx).filter(EventModel.externalId.startswith(externalId)).all()
    except Exception as e:
        print('An error occured (startswith)')
        print(e)
    return dbRecords
def resolve_events_lastchange_starts_with(root, info, lastchange):
    try:
        session = extractSession(info)
        dbRecords = session.query(EventModelEx).filter(EventModel.lastchange.startswith(lastchange)).all()
    except Exception as e:
        print('An error occured (startswith)')
        print(e)
    return dbRecords