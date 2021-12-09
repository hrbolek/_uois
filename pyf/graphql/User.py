from typing_extensions import Required

#from sqlalchemy.sql.sqltypes import Boolean
from graphene import ObjectType, String, Field, ID, List, DateTime, Mutation, Boolean
from functools import cache

@cache
def createGQLUserType(UserModel):
    class UserType(ObjectType):
        id = ID()
        name = String()
        surname = String()
        email = String()

    return UserType

def createGQLUserMutations(UserModel):
    UserType = createGQLUserType(UserModel)

    class CreateUser(Mutation):
        class Arguments:
            id = ID(required=False)
            surname = String(required=False)
            name = String(required=False)
            email = String(required=False)

        ok = Boolean()
        user = Field(UserType)

        def mutate(root, info, id=None, name=None, surname=None, email=None):
            session = extractSession(info)
            dataRecord = UserModel(name=name, surname=surname, email=email)
            session.add(dataRecord)
            session.commit()
            return CreateUser(user=dataRecord, ok=True)

    class UpdateUser(Mutation):
        class Arguments:
            id = ID(required=False)
            surname = String(required=False)
            name = String(required=False)
            email = String(required=False)

        ok = Boolean()
        user = Field(UserType)

        def mutate(root, info, id=None, name=None, surname=None, email=None):
            session = extractSession(info)

            dataRecord = session.query(UserModel).get(id)
            if not(name is None):
                dataRecord.name = name
            if not(surname is None):
                dataRecord.surname = surname
            if not(email is None):
                dataRecord.email = email
            session.commit()

            return CreateUser(user=dataRecord, ok=True)
    result = {
        'add_user': None,
        'update_user': None
    }
    return result

def extendGQLUserType(typesRegistry, UserModel):
    GroupType = typesRegistry.GroupType
    EventType = typesRegistry.EventType
    UserType =  typesRegistry.UserType

    def resolve_groups_by_type(parent, info, typeId):
        session = extractSession(info)
        userRecord = session.query(UserModel).get(parent.id)
        return filter(lambda item: str(item.grouptype_id) == typeId, userRecord.groups)


    def resolve_groups(parent, info):
        session = extractSession(info)
        userRecord = session.query(UserModel).get(parent.id)
        #return [GroupData(group.id, group.name) for group in userRecord.groups]
        return userRecord.groups
    
    def resolve_events(parent, info):
        session = extractSession(info)
        userRecord = session.query(UserModel).get(parent.id)
        return userRecord.events

    
    newAttributes = {
        'groups':  List(GroupType),
        'groups_by_type': Field(List(GroupType), typeId=ID()),
        'events': List(EventType),
        'resolve_groups_by_type': resolve_groups_by_type,
        'resolve_groups': resolve_groups,
        'resolve_events': resolve_events
    }

    for attributeName, attributeValue in newAttributes.items():
        setattr(UserType, attributeName, attributeValue)
    