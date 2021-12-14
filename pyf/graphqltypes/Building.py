from typing_extensions import Required

#from sqlalchemy.sql.sqltypes import Boolean
from graphene import ObjectType, String, Field, ID, List, DateTime, Mutation, Boolean, Int

from models.FacilitiesRelated.BuildingModel import BuildingModel
from models.FacilitiesRelated.ArealModel import ArealModel
from models.FacilitiesRelated.RoomModel import RoomModel

from graphqltypes.Utils import extractSession

class BuildingType(ObjectType):
    id = ID()

    lastchange = DateTime()
    externalId = String()
    name = String()

    areal = Field('graphqltypes.Areal.ArealType')
    rooms = List('graphqltypes.Room.RoomType')

    def resolve_areal(parent, info):
        session = extractSession(info)
        dbRecord = session.query(BuildingModel).get(parent.id)
        return dbRecord.areal

    def resolve_rooms(parent, info):
        session = extractSession(info)
        dbRecords = session.query(RoomModel).filter_by(building_id=parent.id).all()
        return dbRecords
        

    
