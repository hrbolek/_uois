import graphene
from sqlalchemy.orm import relationship
from BaseModel import BaseModel

def extractSession(info):
    #return info.context['request'].scope['db_session']
    assert not info.context is None, 'Got Bad Context'
    return info.context.get('session')

class EventUserModel(BaseModel):
    __tablename__ = 'events_users'
    __table_args__ = {'extend_existing': True} 
    
    usermodel = relationship('UserModel')
    # usermodel = association_proxy('usermodel', 'keyword')
    eventmodel = relationship('EventModel')
    # eventmodel = association_proxy('eventmodel', 'keyword')


class get_EventUserModel(graphene.ObjectType):
    
    id = graphene.String()
    user_id = graphene.String()
    event_id = graphene.String()
    
        
    usermodel = graphene.Field('gql_UserModel.get_UserModel')
    def resolver_usermodel(parent, info):
        return parent.usermodel
        
    eventmodel = graphene.Field('gql_EventModel.get_EventModel')
    def resolver_eventmodel(parent, info):
        return parent.eventmodel


class create_EventUserModel(graphene.Mutation):
    class Arguments:
        id = graphene.String(required=True)
        user_id = graphene.String(required=True)
        event_id = graphene.String(required=True)

    ok = graphene.Boolean()
    result = graphene.Field('get_EventUserModel')
    
    def mutate(parent, info, **paramList):
        session = extractSession(info)
        result = EventUserModel(**paramList)
        session.add(result)
        session.commit()
        return create_EventUserModel(ok=True, result=result)
    pass

class update_EventUserModel(graphene.Mutation):
    class Arguments:
        id = graphene.String(required=True)    
        user_id = graphene.String(required=False)    
        event_id = graphene.String(required=False)

    ok = graphene.Boolean()
    result = graphene.Field('get_EventUserModel')
    
    def mutate(parent, info, **paramList):
        session = extractSession(info)
        dbRecord = session.query(EventUserModel).filter_by(id=paramList['id']).one()
        for key, item in paramList.items():
            if key=='id':
                continue
            setattr(dbRecord, key, item)
        session.commit()
        return update_EventUserModel(ok=True, result=dbRecord)
    pass


def resolve_events_users_by_id(root, info, id):
    session = extractSession(info)
    dbRecord = session.query(EventUserModel).filter_by(id=id).one()
    return dbRecord
def resolve_events_users_user_id_starts_with(root, info, user_id):
    session = extractSession(info)
    dbRecords = session.query(EventUserModel).filter(EventUserModel.user_id.startswith(user_id)).all()
    return dbRecords
def resolve_events_users_event_id_starts_with(root, info, event_id):
    session = extractSession(info)
    dbRecords = session.query(EventUserModel).filter(EventUserModel.event_id.startswith(event_id)).all()
    return dbRecords