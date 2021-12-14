from typing_extensions import Required

from graphene import ObjectType, String, Field, ID, List, DateTime, Mutation, Boolean, Int, NonNull

#from models.GroupRelated.GroupModel import GroupModel
from graphqltypes.Utils import extractSession

from graphqltypes.Utils import createRootResolverById, createRootResolverByName
from models.AcreditationRelated.SubjectSemesterModel import SubjectSemesterModel

class SubjectSemesterType(ObjectType):
    id = ID()
    name = String()

    lastchange = DateTime()
    externalId = String()

    subject = Field('graphqltypes.SubjectSemester.SubjectSemesterType')

    topics = List('graphqltypes.SubjectSemesterTopic.SubjectSemesterTopicType')
    def resolve_topics(parent, info):
        session = extractSession(info)
        #groupRecord = session.query(GroupModel).get(parent.id)
        try:
            dbRecord = session.query(SubjectSemesterModel).filter_by(id=parent.id).one()
            result = dbRecord.topics
        except Exception as e:
            print('@resolve_topics', e)
        return result
        
