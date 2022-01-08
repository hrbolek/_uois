import graphene
from sqlalchemy.orm import relationship
from BaseModel import BaseModel

def extractSession(info):
    #return info.context['request'].scope['db_session']
    assert not info.context is None, 'Got Bad Context'
    return info.context.get('session')

class StudyPlanItemEventModel(BaseModel):
    __tablename__ = 'studyplanitem_events'
    __table_args__ = {'extend_existing': True} 
    
    eventmodel = relationship('EventModel')
    # eventmodel = association_proxy('eventmodel', 'keyword')
    studyplanitemmodel = relationship('StudyPlanItemModel')
    # studyplanitemmodel = association_proxy('studyplanitemmodel', 'keyword')


class get_StudyPlanItemEventModel(graphene.ObjectType):
    
    id = graphene.String()
    studyplanitem_id = graphene.String()
    event_id = graphene.String()
    
        
    eventmodel = graphene.Field('gql_EventModel.get_EventModel')
    def resolver_eventmodel(parent, info):
        return parent.eventmodel
        
    studyplanitemmodel = graphene.Field('gql_StudyPlanItemModel.get_StudyPlanItemModel')
    def resolver_studyplanitemmodel(parent, info):
        return parent.studyplanitemmodel


class create_StudyPlanItemEventModel(graphene.Mutation):
    class Arguments:
        id = graphene.String(required=True)
        studyplanitem_id = graphene.String(required=True)
        event_id = graphene.String(required=True)

    ok = graphene.Boolean()
    result = graphene.Field('get_StudyPlanItemEventModel')
    
    def mutate(parent, info, **paramList):
        session = extractSession(info)
        result = StudyPlanItemEventModel(**paramList)
        session.add(result)
        session.commit()
        return create_StudyPlanItemEventModel(ok=True, result=result)
    pass

class update_StudyPlanItemEventModel(graphene.Mutation):
    class Arguments:
        id = graphene.String(required=True)    
        studyplanitem_id = graphene.String(required=False)    
        event_id = graphene.String(required=False)

    ok = graphene.Boolean()
    result = graphene.Field('get_StudyPlanItemEventModel')
    
    def mutate(parent, info, **paramList):
        session = extractSession(info)
        dbRecord = session.query(StudyPlanItemEventModel).filter_by(id=paramList['id']).one()
        for key, item in paramList.items():
            if key=='id':
                continue
            setattr(dbRecord, key, item)
        session.commit()
        return update_StudyPlanItemEventModel(ok=True, result=dbRecord)
    pass


def resolve_studyplanitem_events_by_id(root, info, id):
    session = extractSession(info)
    dbRecord = session.query(StudyPlanItemEventModel).filter_by(id=id).one()
    return dbRecord
def resolve_studyplanitem_events_studyplanitem_id_starts_with(root, info, studyplanitem_id):
    session = extractSession(info)
    dbRecords = session.query(StudyPlanItemEventModel).filter(StudyPlanItemEventModel.studyplanitem_id.startswith(studyplanitem_id)).all()
    return dbRecords
def resolve_studyplanitem_events_event_id_starts_with(root, info, event_id):
    session = extractSession(info)
    dbRecords = session.query(StudyPlanItemEventModel).filter(StudyPlanItemEventModel.event_id.startswith(event_id)).all()
    return dbRecords