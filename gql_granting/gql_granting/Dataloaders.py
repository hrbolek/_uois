from uoishelpers.dataloaders import createIdLoader, createFkeyLoader
from functools import cache

from gql_granting.DBDefinitions import (
    ProgramFormTypeModel,
    ProgramGroupModel,
    ProgramLanguageTypeModel,
    ProgramLevelTypeModel,
    ProgramModel,
    ProgramTitleTypeModel,
    ProgramTypeModel,
    ProgramStudents,

    ClassificationLevelModel,
    ClassificationModel,
    ClassificationTypeModel,
    
    SubjectModel,
    SemesterModel,
    TopicModel,
    LessonModel,
    LessonTypeModel
)
async def createLoaders_3(asyncSessionMaker):

    class Loaders:
        @property
        @cache
        def acprogramform_by_id(self):
            return createIdLoader(asyncSessionMaker, ProgramFormTypeModel)

        @property
        @cache
        def acprogramlanguage_by_id(self):
            return createIdLoader(asyncSessionMaker, ProgramLanguageTypeModel)

        @property
        @cache
        def acprogramlevel_by_id(self):
            return createIdLoader(asyncSessionMaker, ProgramLevelTypeModel)

        @property
        @cache
        def acprogramtitle_by_id(self):
            return createIdLoader(asyncSessionMaker, ProgramTitleTypeModel)

        @property
        @cache
        def acprogramtype_by_id(self):
            return createIdLoader(asyncSessionMaker, ProgramTypeModel)

        @property
        @cache
        def acclassificationlevel_by_id(self):
            return createIdLoader(asyncSessionMaker, ClassificationLevelModel)

        @property
        @cache
        def acclassificationtype_by_id(self):
            return createIdLoader(asyncSessionMaker, ClassificationTypeModel)

        @property
        @cache
        def aclessontype_by_id(self):
            return createIdLoader(asyncSessionMaker, LessonTypeModel)

        @property
        @cache
        def acprogramgroup_by_id(self):
            return createIdLoader(asyncSessionMaker, ProgramGroupModel)

        @property
        @cache
        def acprogram_by_id(self):
            return createIdLoader(asyncSessionMaker, ProgramModel)

        @property
        @cache
        def acsubject_by_id(self):
            return createIdLoader(asyncSessionMaker, SubjectModel)

        @property
        @cache
        def acsubject_for_program(self):
            return createFkeyLoader(asyncSessionMaker, SubjectModel, foreignKeyName="program_id")

        @property
        @cache
        def acsemester_for_subject(self):
            return createFkeyLoader(asyncSessionMaker, SemesterModel, foreignKeyName="subject_id")

        @property
        @cache
        def acsemester_by_id(self):
            return createIdLoader(asyncSessionMaker, SemesterModel)

        @property
        @cache
        def actopic_by_id(self):
            return createIdLoader(asyncSessionMaker, TopicModel)

        @property
        @cache
        def actopics_for_semester(self):
            return createFkeyLoader(asyncSessionMaker, TopicModel, foreignKeyName="semester_id")

        @property
        @cache
        def aclesson_by_id(self):
            return createIdLoader(asyncSessionMaker, LessonModel)

        @property
        @cache
        def aclessons_for_topic(self):
            return createFkeyLoader(asyncSessionMaker, LessonModel, foreignKeyName="topic_id")

        @property
        @cache
        def acclassification_by_id(self):
            return createIdLoader(asyncSessionMaker, ClassificationModel)

        @property
        @cache
        def acclassification_for_semester(self):
            return createFkeyLoader(asyncSessionMaker, ClassificationModel, foreignKeyName="semester_id")

    return Loaders()

dbmodels = {
    "programforms": ProgramFormTypeModel,
    "programgroups": ProgramGroupModel,
    "programlanguages": ProgramLanguageTypeModel,
    "programleveltypes": ProgramLevelTypeModel,
    "programs": ProgramModel,
    "programtitletypes": ProgramTitleTypeModel,
    "programtypes": ProgramTypeModel,
    "programstudents": ProgramStudents,

    "classificationlevels": ClassificationLevelModel,
    "classifications": ClassificationModel,
    "classificationtypes": ClassificationTypeModel,
    
    "subjects": SubjectModel,
    "semesters": SemesterModel,
    "topics": TopicModel,
    "lessons": LessonModel,
    "lessontypes": LessonTypeModel
}

async def createLoaders(asyncSessionMaker, models=dbmodels):
    def createLambda(loaderName, DBModel):
        return lambda self: createIdLoader(asyncSessionMaker, DBModel)
    
    attrs = {}
    for key, DBModel in models.items():
        attrs[key] = property(cache(createLambda(key, DBModel)))
    
    Loaders = type('Loaders', (), attrs)   
    return Loaders()