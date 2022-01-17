import graphene
from sqlalchemy.orm import relationship
from BaseModel import BaseModel

def extractSession(info):
    #return info.context['request'].scope['db_session']
    assert not info.context is None, 'Got Bad Context'
    return info.context.get('session')

class StudyPlanItemModelEx(BaseModel):
    __tablename__ = 'studyplanitems'
    __table_args__ = {'extend_existing': True} 
    
    studyplanmodel = relationship('StudyPlanModelEx')
    # studyplanmodel = association_proxy('studyplanmodel', 'keyword')
    studyplanitemeventmodels = relationship('StudyPlanItemEventModelEx')
    # studyplanitemeventmodels = association_proxy('studyplanitemeventmodels', 'keyword')
    studyplanitemteachermodels = relationship('StudyPlanItemTeacherModelEx')
    # studyplanitemteachermodels = association_proxy('studyplanitemteachermodels', 'keyword')
    studyplanitemgroupmodels = relationship('StudyPlanItemGroupModelEx')
    # studyplanitemgroupmodels = association_proxy('studyplanitemgroupmodels', 'keyword')


class StudyPlanItemModel(graphene.ObjectType):
    
    id = graphene.String()
    name = graphene.String()
    priority = graphene.Int()
    subjectSemesterTopic = graphene.String()
    externalId = graphene.String()
    studyplan_id = graphene.String()
    
        
    studyplanmodel = graphene.Field('graphqltypes.gql_StudyPlanModel.StudyPlanModel')
    def resolver_studyplanmodel(parent, info):
        return parent.studyplanmodel
        
    studyplanitemeventmodels = graphene.List('graphqltypes.gql_StudyPlanItemEventModel.StudyPlanItemEventModel')
        
    def resolver_studyplanitemeventmodels(parent, info):
        return parent.studyplanitemeventmodels
        
    studyplanitemteachermodels = graphene.List('graphqltypes.gql_StudyPlanItemTeacherModel.StudyPlanItemTeacherModel')
        
    def resolver_studyplanitemteachermodels(parent, info):
        return parent.studyplanitemteachermodels
        
    studyplanitemgroupmodels = graphene.List('graphqltypes.gql_StudyPlanItemGroupModel.StudyPlanItemGroupModel')
        
    def resolver_studyplanitemgroupmodels(parent, info):
        return parent.studyplanitemgroupmodels


class create_StudyPlanItemModel(graphene.Mutation):
    class Arguments:
        id = graphene.String(required=True)
        name = graphene.String(required=True)
        priority = graphene.Int(required=True)
        subjectSemesterTopic = graphene.String(required=True)
        externalId = graphene.String(required=True)
        studyplan_id = graphene.String(required=True)

    ok = graphene.Boolean()
    result = graphene.Field('graphqltypes.gql_StudyPlanItemModel.StudyPlanItemModel')
    
    def mutate(parent, info, **paramList):
        session = extractSession(info)
        result = StudyPlanItemModelEx(**paramList)
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
    result = graphene.Field('graphqltypes.gql_StudyPlanItemModel.StudyPlanItemModel')
    
    def mutate(parent, info, **paramList):
        session = extractSession(info)
        dbRecord = session.query(StudyPlanItemModelEx).filter_by(id=paramList['id']).one()
        for key, item in paramList.items():
            if key=='id':
                continue
            setattr(dbRecord, key, item)
        session.commit()
        return update_StudyPlanItemModel(ok=True, result=dbRecord)
    pass

def to_dict(row):
    return {column.name: getattr(row, row.__mapper__.get_property_by_column(column).key) for column in row.__table__.columns}


def resolve_studyplanitems_by_id(root, info, id):
    try:
        session = extractSession(info)
        dbRecord = session.query(StudyPlanItemModelEx).filter_by(id=id).one()
    except Exception as e:
        print('An error occured (by_id)')
        print(e)
    print(f'to_dict(dbRecord)')
    return dbRecord
def resolve_studyplanitems_name_starts_with(root, info, name):
    try:
        session = extractSession(info)
        dbRecords = session.query(StudyPlanItemModelEx).filter(StudyPlanItemModel.name.startswith(name)).all()
    except Exception as e:
        print('An error occured (startswith)')
        print(e)
    return dbRecords
def resolve_studyplanitems_priority_starts_with(root, info, priority):
    try:
        session = extractSession(info)
        dbRecords = session.query(StudyPlanItemModelEx).filter(StudyPlanItemModel.priority.startswith(priority)).all()
    except Exception as e:
        print('An error occured (startswith)')
        print(e)
    return dbRecords
def resolve_studyplanitems_subjectSemesterTopic_starts_with(root, info, subjectSemesterTopic):
    try:
        session = extractSession(info)
        dbRecords = session.query(StudyPlanItemModelEx).filter(StudyPlanItemModel.subjectSemesterTopic.startswith(subjectSemesterTopic)).all()
    except Exception as e:
        print('An error occured (startswith)')
        print(e)
    return dbRecords
def resolve_studyplanitems_externalId_starts_with(root, info, externalId):
    try:
        session = extractSession(info)
        dbRecords = session.query(StudyPlanItemModelEx).filter(StudyPlanItemModel.externalId.startswith(externalId)).all()
    except Exception as e:
        print('An error occured (startswith)')
        print(e)
    return dbRecords
def resolve_studyplanitems_studyplan_id_starts_with(root, info, studyplan_id):
    try:
        session = extractSession(info)
        dbRecords = session.query(StudyPlanItemModelEx).filter(StudyPlanItemModel.studyplan_id.startswith(studyplan_id)).all()
    except Exception as e:
        print('An error occured (startswith)')
        print(e)
    return dbRecords