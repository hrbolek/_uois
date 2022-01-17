

import random
from typing_extensions import Required

#from sqlalchemy.sql.sqltypes import Boolean
from graphene import ObjectType, String, Field, ID, List, DateTime, Mutation, Boolean, Int

from models.AcreditationRelated.StudyPlan import StudyPlanModel
from models.AcreditationRelated.StudyPlanItem import StudyPlanItemModel

from graphqltypes.Utils import extractSession

from graphqltypes.Utils import createRootResolverById, createRootResolverByName, createMutationClass

StudyPlanRootResolverById = createRootResolverById(StudyPlanModel)
StudyPlanRootResolverByName = createRootResolverByName(StudyPlanModel)

CreateStudyPlan = createMutationClass(
        StudyPlanModel, Field('graphqltypes.StudyPlan.StudyPlanType'), parentItemName=None, 
        name = String()
        )

class StudyPlanType(ObjectType):
    id = ID()

    lastchange = DateTime()
    externalId = String()
    name = String()

    studyplanitems = List('graphqltypes.StudyPlan.StudyPlanItemType')

    create_new_item = createMutationClass(
        StudyPlanItemModel, Field('graphqltypes.StudyPlan.StudyPlanItemType'), parentItemName='studyplan', 
        name = String()
        ).Field()

    def resolve_studyplanitems(parent, info):
        if hasattr(parent, 'studyplanitems'):
            result = parent.studyplanitems
        else:
            session = extractSession(info)
            result = session.query(StudyPlanItemModel).filter(StudyPlanItemModel.studyplan_id == parent.id).all()
        return result
        
class StudyPlanItemType(ObjectType):
    id = ID()
    name = String()
    studyplan = Field('graphqltypes.StudyPlan.StudyPlanType')
    itemevents = List('graphqltypes.StudyPlan.StudyPlanItemEventType')

class StudyPlanItemEventType(ObjectType):
    id = ID()
    name = String()
    studyplanitem = Field('graphqltypes.StudyPlan.StudyPlanItemType')


from models.AcreditationRelated.ProgramModel import ProgramModel
from models.GroupRelated.GroupModel import GroupModel

def createRandomStudyPlans(Mutation):
    class Arguments():
        programId = Int()
        pass

    result = List('graphqltypes.StudyPlan.StudyPlanType')
    ok = Boolean()

    def mutate(root, info, programId):
        session = extractSession(info)
        program = session.query(ProgramModel).filter_by(id=programId).one()
        subjects = program.subjects
        studyGroups = list(session.query(GroupModel).filter(GroupModel.grouptype_id == 3).all())

        for subject, studyGroup in zip(subjects, studyGroups):
            studyPlan = StudyPlanModel(subject.name)
            session.add(studyPlan)
            session.commit()

            semester = subject.subjectsemesters[0]
            for topic in semester.topics:
                planItem = StudyPlanItemModel(name=topic.name, studyplan_id=studyPlan.id)
                session.add(planItem)
                session.commit()

        return createRandomStudyPlans(ok=True, result=[])
