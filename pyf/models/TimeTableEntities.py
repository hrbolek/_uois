from sqlalchemy import Column, String, BigInteger, Integer, DateTime, ForeignKey, Sequence
import datetime
from functools import cache

#unitedSequence = Sequence('all_id_seq')
from . import BaseModel

@cache # funny thing, it makes from this function a singleton
def GetModels(BaseModel=BaseModel.getBaseModel(), unitedSequence=Sequence('all_id_seq')):
    #assert not(unitedSequence is None), "unitedSequence must be defined"

    class EventModel(BaseModel):
        __tablename__ = 'events'
        
        id = Column(BigInteger, unitedSequence, primary_key=True)
        start = Column(DateTime)
        end = Column(DateTime)
        label = Column(String)
        externalId = Column(String, index=True)
        lastchange = Column(DateTime, default=datetime.datetime.now)

    return EventModel

@cache
def BuildRelations():

    from . import BaseEntities
    from . import FacilityEntities

    from . import Relations 

    UserModel, GroupModel, RoleModel, GroupTypeModel, RoleTypeModel = BaseEntities.GetModels()
    AreaModel, BuildingModel, RoomModel = FacilityEntities.GetModels()
    EventModel = GetModels()

    Relations.defineRelationNM(UserModel, EventModel)
    Relations.defineRelationNM(GroupModel, EventModel)
    Relations.defineRelation1N(EventModel, RoomModel)

    pass