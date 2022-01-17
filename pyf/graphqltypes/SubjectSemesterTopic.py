from typing_extensions import Required

from graphene import ObjectType, String, Field, ID, List, DateTime, Mutation, Boolean, Int, NonNull

#from models.GroupRelated.GroupModel import GroupModel
from graphqltypes.Utils import extractSession
from models.AcreditationRelated.SubjectTopic import SubjectTopicModel
from graphqltypes.Utils import createRootResolverById, createRootResolverByName

SubjectSemesterTopicRootResolverById = createRootResolverById(SubjectTopicModel)

class SubjectSemesterTopicType(ObjectType):
    id = ID()
    name = String()

    lastchange = DateTime()
    externalId = String()
        
