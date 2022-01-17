from typing_extensions import Required

from graphene import ObjectType, String, Field, ID, List, DateTime, Mutation, Boolean, Int, NonNull

#from models.GroupRelated.GroupModel import GroupModel
from graphqltypes.Utils import extractSession

from graphqltypes.Utils import createRootResolverById, createRootResolverByName
from models.AcreditationRelated.SubjectModel import SubjectModel

from graphqltypes.Utils import createRootResolverById, createRootResolverByName

SubjectRootResolverById = createRootResolverById(SubjectModel)
SubjectRootResolverByName = createRootResolverByName(SubjectModel)

class SubjectType(ObjectType):
    id = ID()
    name = String()

    lastchange = DateTime()
    externalId = String()

    program = Field('graphqltypes.Program.ProgramType')

    semesters = List('graphqltypes.SubjectSemester.SubjectSemesterType')
    def resolve_semesters(parent, info):
        session = extractSession(info)
        #groupRecord = session.query(GroupModel).get(parent.id)
        try:
            dbRecord = session.query(SubjectModel).filter_by(id=parent.id).one()
            result = dbRecord.subjectsemesters
        except Exception as e:
            print(f"@resolve_semesters {parent.id}", e)

        return result
        
