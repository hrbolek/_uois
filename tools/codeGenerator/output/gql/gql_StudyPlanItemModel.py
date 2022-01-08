import graphene
from sqlalchemy.orm import relationship
from BaseModel import BaseModel

def extractSession(info):
    #return info.context['request'].scope['db_session']
    assert not info.context is None, 'Got Bad Context'
    return info.context.get('session')

class StudyPlanItemModel(BaseModel):
    __tablename__ = 'studyplanitems'
    __table_args__ = {'extend_existing': True} 
    
    studyplanmodel = relationship('StudyPlanModel')
    # studyplanmodel = association_proxy('studyplanmodel', 'keyword')
    studyplanitemeventmodel_collection = relationship('StudyPlanItemEventModel')
    # studyplanitemeventmodel_collection = association_proxy('studyplanitemeventmodel_collection', 'keyword')
    studyplanitemteachermodel_collection = relationship('StudyPlanItemTeacherModel')
    # studyplanitemteachermodel_collection = association_proxy('studyplanitemteachermodel_collection', 'keyword')
    studyplanitemgroupmodel_collection = relationship('StudyPlanItemGroupModel')
    # studyplanitemgroupmodel_collection = association_proxy('studyplanitemgroupmodel_collection', 'keyword')


class get_StudyPlanItemModel(graphene.ObjectType):
    
    id = graphene.String()
    name = graphene.String()
    priority = graphene.Int()
    subjectSemesterTopic = graphene.String()
    externalId = graphene.String()
    studyplan_id = graphene.String()
    
        
    studyplanmodel = graphene.Field('gql_StudyPlanModel.get_StudyPlanModel')
    def resolver_studyplanmodel(parent, info):
        return parent.studyplanmodel
        
    studyplanitemeventmodel_collection = graphene.List('gql_StudyPlanItemEventModel.get_StudyPlanItemEventModel')
        
    def resolver_studyplanitemeventmodel_collection(parent, info):
        return parent.studyplanitemeventmodel_collection
        
    studyplanitemteachermodel_collection = graphene.List('gql_StudyPlanItemTeacherModel.get_StudyPlanItemTeacherModel')
        
    def resolver_studyplanitemteachermodel_collection(parent, info):
        return parent.studyplanitemteachermodel_collection
        
    studyplanitemgroupmodel_collection = graphene.List('gql_StudyPlanItemGroupModel.get_StudyPlanItemGroupModel')
        
    def resolver_studyplanitemgroupmodel_collection(parent, info):
        return parent.studyplanitemgroupmodel_collection


class create_StudyPlanItemModel(graphene.Mutation):
    class Arguments:
        id = graphene.String(required=True)
        name = graphene.String(required=True)
        priority = graphene.Int(required=True)
        subjectSemesterTopic = graphene.String(required=True)
        externalId = graphene.String(required=True)
        studyplan_id = graphene.String(required=True)

    ok = graphene.Boolean()
    result = graphene.Field('get_StudyPlanItemModel')
    
    def mutate(parent, info, **paramList):
        session = extractSession(info)
        result = StudyPlanItemModel(**paramList)
        session.add(result)
        session.commit()
        return create_StudyPlanItemModel(ok=True, result=result)
    pass

class update_StudyPlanItemModel(graphene.Mutation):
    class Arguments:
        id = graphene.String(required=True)    
        name = graphene.String(required=False)    
        priority = graphene.Int(required=False)    
        subjectSemesterTopic = graphene.String(required=False)    
        externalId = graphene.String(required=False)    
        studyplan_id = graphene.String(required=False)

    ok = graphene.Boolean()
    result = graphene.Field('get_StudyPlanItemModel')
    
    def mutate(parent, info, **paramList):
        session = extractSession(info)
        dbRecord = session.query(StudyPlanItemModel).filter_by(id=paramList['id']).one()
        for key, item in paramList.items():
            if key=='id':
                continue
            setattr(dbRecord, key, item)
        session.commit()
        return update_StudyPlanItemModel(ok=True, result=dbRecord)
    pass


def resolve_studyplanitems_by_id(root, info, id):
    session = extractSession(info)
    dbRecord = session.query(StudyPlanItemModel).filter_by(id=id).one()
    return dbRecord
def resolve_studyplanitems_name_starts_with(root, info, name):
    session = extractSession(info)
    dbRecords = session.query(StudyPlanItemModel).filter(StudyPlanItemModel.name.startswith(name)).all()
    return dbRecords
def resolve_studyplanitems_priority_starts_with(root, info, priority):
    session = extractSession(info)
    dbRecords = session.query(StudyPlanItemModel).filter(StudyPlanItemModel.priority.startswith(priority)).all()
    return dbRecords
def resolve_studyplanitems_subjectSemesterTopic_starts_with(root, info, subjectSemesterTopic):
    session = extractSession(info)
    dbRecords = session.query(StudyPlanItemModel).filter(StudyPlanItemModel.subjectSemesterTopic.startswith(subjectSemesterTopic)).all()
    return dbRecords
def resolve_studyplanitems_externalId_starts_with(root, info, externalId):
    session = extractSession(info)
    dbRecords = session.query(StudyPlanItemModel).filter(StudyPlanItemModel.externalId.startswith(externalId)).all()
    return dbRecords
def resolve_studyplanitems_studyplan_id_starts_with(root, info, studyplan_id):
    session = extractSession(info)
    dbRecords = session.query(StudyPlanItemModel).filter(StudyPlanItemModel.studyplan_id.startswith(studyplan_id)).all()
    return dbRecords