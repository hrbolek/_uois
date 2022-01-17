import graphene
from sqlalchemy.orm import relationship
from BaseModel import BaseModel

def extractSession(info):
    #return info.context['request'].scope['db_session']
    assert not info.context is None, 'Got Bad Context'
    return info.context.get('session')

class EventUserModelEx(BaseModel):
    __tablename__ = 'events_users'
    __table_args__ = {'extend_existing': True} 
    
    usermodel = relationship('UserModelEx')
    # usermodel = association_proxy('usermodel', 'keyword')
    eventmodel = relationship('EventModelEx')
    # eventmodel = association_proxy('eventmodel', 'keyword')


class EventUserModel(graphene.ObjectType):
    
    id = graphene.String()
    user_id = graphene.String()
    event_id = graphene.String()
    
        
    usermodel = graphene.Field('graphqltypes.gql_UserModel.UserModel')
    def resolver_usermodel(parent, info):
        return parent.usermodel
        
    eventmodel = graphene.Field('graphqltypes.gql_EventModel.EventModel')
    def resolver_eventmodel(parent, info):
        return parent.eventmodel


class create_EventUserModel(graphene.Mutation):
    class Arguments:
        id = graphene.String(required=True)
        user_id = graphene.String(required=True)
        event_id = graphene.String(required=True)

    ok = graphene.Boolean()
    result = graphene.Field('graphqltypes.gql_EventUserModel.EventUserModel')
    
    def mutate(parent, info, **paramList):
        session = extractSession(info)
        result = EventUserModelEx(**paramList)
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
    result = graphene.Field('graphqltypes.gql_EventUserModel.EventUserModel')
    
    def mutate(parent, info, **paramList):
        session = extractSession(info)
        dbRecord = session.query(EventUserModelEx).filter_by(id=paramList['id']).one()
        for key, item in paramList.items():
            if key=='id':
                continue
            setattr(dbRecord, key, item)
        session.commit()
        return update_EventUserModel(ok=True, result=dbRecord)
    pass

def to_dict(row):
    return {column.name: getattr(row, row.__mapper__.get_property_by_column(column).key) for column in row.__table__.columns}


def resolve_events_users_by_id(root, info, id):
    try:
        session = extractSession(info)
        dbRecord = session.query(EventUserModelEx).filter_by(id=id).one()
    except Exception as e:
        print('An error occured (by_id)')
        print(e)
    print(f'to_dict(dbRecord)')
    return dbRecord
def resolve_events_users_user_id_starts_with(root, info, user_id):
    try:
        session = extractSession(info)
        dbRecords = session.query(EventUserModelEx).filter(EventUserModel.user_id.startswith(user_id)).all()
    except Exception as e:
        print('An error occured (startswith)')
        print(e)
    return dbRecords
def resolve_events_users_event_id_starts_with(root, info, event_id):
    try:
        session = extractSession(info)
        dbRecords = session.query(EventUserModelEx).filter(EventUserModel.event_id.startswith(event_id)).all()
    except Exception as e:
        print('An error occured (startswith)')
        print(e)
    return dbRecords