import graphene
from sqlalchemy.orm import relationship
from BaseModel import BaseModel

def extractSession(info):
    #return info.context['request'].scope['db_session']
    assert not info.context is None, 'Got Bad Context'
    return info.context.get('session')

class EventGroupModelEx(BaseModel):
    __tablename__ = 'events_groups'
    __table_args__ = {'extend_existing': True} 
    
    eventmodel = relationship('EventModelEx')
    # eventmodel = association_proxy('eventmodel', 'keyword')
    groupmodel = relationship('GroupModelEx')
    # groupmodel = association_proxy('groupmodel', 'keyword')


class EventGroupModel(graphene.ObjectType):
    
    id = graphene.String()
    group_id = graphene.String()
    event_id = graphene.String()
    
        
    eventmodel = graphene.Field('graphqltypes.gql_EventModel.EventModel')
    def resolver_eventmodel(parent, info):
        return parent.eventmodel
        
    groupmodel = graphene.Field('graphqltypes.gql_GroupModel.GroupModel')
    def resolver_groupmodel(parent, info):
        return parent.groupmodel


class create_EventGroupModel(graphene.Mutation):
    class Arguments:
        id = graphene.String(required=True)
        group_id = graphene.String(required=True)
        event_id = graphene.String(required=True)

    ok = graphene.Boolean()
    result = graphene.Field('graphqltypes.gql_EventGroupModel.EventGroupModel')
    
    def mutate(parent, info, **paramList):
        session = extractSession(info)
        result = EventGroupModelEx(**paramList)
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
    result = graphene.Field('graphqltypes.gql_EventGroupModel.EventGroupModel')
    
    def mutate(parent, info, **paramList):
        session = extractSession(info)
        dbRecord = session.query(EventGroupModelEx).filter_by(id=paramList['id']).one()
        for key, item in paramList.items():
            if key=='id':
                continue
            setattr(dbRecord, key, item)
        session.commit()
        return update_EventGroupModel(ok=True, result=dbRecord)
    pass

def to_dict(row):
    return {column.name: getattr(row, row.__mapper__.get_property_by_column(column).key) for column in row.__table__.columns}


def resolve_events_groups_by_id(root, info, id):
    try:
        session = extractSession(info)
        dbRecord = session.query(EventGroupModelEx).filter_by(id=id).one()
    except Exception as e:
        print('An error occured (by_id)')
        print(e)
    print(f'to_dict(dbRecord)')
    return dbRecord
def resolve_events_groups_group_id_starts_with(root, info, group_id):
    try:
        session = extractSession(info)
        dbRecords = session.query(EventGroupModelEx).filter(EventGroupModel.group_id.startswith(group_id)).all()
    except Exception as e:
        print('An error occured (startswith)')
        print(e)
    return dbRecords
def resolve_events_groups_event_id_starts_with(root, info, event_id):
    try:
        session = extractSession(info)
        dbRecords = session.query(EventGroupModelEx).filter(EventGroupModel.event_id.startswith(event_id)).all()
    except Exception as e:
        print('An error occured (startswith)')
        print(e)
    return dbRecords