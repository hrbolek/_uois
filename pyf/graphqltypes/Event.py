from typing_extensions import Required

#from sqlalchemy.sql.sqltypes import Boolean
from graphene import ObjectType, String, Field, ID, List, DateTime, Mutation, Boolean, Int

from models.EventsRelated.EventModel import EventModel
from graphqltypes.Utils import extractSession

class EventType(ObjectType):
    id = ID()
    name = String()

    lastchange = DateTime()
    externalId = String()

    users = List('graphqltypes.User.UserType')
    def resolve_users(parent, info):
        session = extractSession(info)
        dbRecord = session.query(EventModel).get(parent.id)
        return dbRecord.users
        
    groups = List('graphqltypes.Group.GroupType')
    def resolve_users(parent, info):
        session = extractSession(info)
        dbRecord = session.query(EventModel).get(parent.id)
        return dbRecord.groups
        
    rooms = List('graphqltypes.Room.RoomType')
    def resolve_rooms(parent, info):
        session = extractSession(info)
        dbRecord = session.query(EventModel).get(parent.id)
        return dbRecord.rooms
