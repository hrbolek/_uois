from typing_extensions import Required

#from sqlalchemy.sql.sqltypes import Boolean
from graphene import ObjectType, String, Field, ID, List, DateTime, Mutation, Boolean, Int

from models.FacilitiesRelated.BuildingModel import BuildingModel
from models.FacilitiesRelated.ArealModel import ArealModel
from models.FacilitiesRelated.RoomModel import RoomModel

from graphqltypes.Utils import extractSession

from graphqltypes.Utils import createRootResolverById, createRootResolverByName

BuildingRootResolverById = createRootResolverById(BuildingModel)
BuildingRootResolverByName = createRootResolverByName(BuildingModel)

class BuildingType(ObjectType):
    id = ID()

    lastchange = DateTime()
    externalId = String()
    name = String()

    areal = Field('graphqltypes.Areal.ArealType')
    rooms = List('graphqltypes.Room.RoomType')

    def resolve_areal(parent, info):
        if hasattr(parent, 'areal'):
            result = parent.areal
        else:
            session = extractSession(info)
            dbRecord = session.query(BuildingModel).get(parent.id)
            result = dbRecord.areal
        return result

    def resolve_rooms(parent, info):
        if hasattr(parent, 'rooms'):
            result = parent.rooms
        else:
            session = extractSession(info)
            result = session.query(RoomModel).filter_by(building_id=parent.id).all()
        return result
        

    
