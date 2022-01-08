import graphene
from sqlalchemy.orm import relationship
from BaseModel import BaseModel

def extractSession(info):
    #return info.context['request'].scope['db_session']
    assert not info.context is None, 'Got Bad Context'
    return info.context.get('session')

class StudyPlanItemTeacherModel(BaseModel):
    __tablename__ = 'studyplanitem_teachers'
    __table_args__ = {'extend_existing': True} 
    
    studyplanitemmodel = relationship('StudyPlanItemModel')
    # studyplanitemmodel = association_proxy('studyplanitemmodel', 'keyword')
    usermodel = relationship('UserModel')
    # usermodel = association_proxy('usermodel', 'keyword')


class get_StudyPlanItemTeacherModel(graphene.ObjectType):
    
    id = graphene.String()
    teacher_id = graphene.String()
    studyplanitem_id = graphene.String()
    
        
    studyplanitemmodel = graphene.Field('gql_StudyPlanItemModel.get_StudyPlanItemModel')
    def resolver_studyplanitemmodel(parent, info):
        return parent.studyplanitemmodel
        
    usermodel = graphene.Field('gql_UserModel.get_UserModel')
    def resolver_usermodel(parent, info):
        return parent.usermodel


class create_StudyPlanItemTeacherModel(graphene.Mutation):
    class Arguments:
        id = graphene.String(required=True)
        teacher_id = graphene.String(required=True)
        studyplanitem_id = graphene.String(required=True)

    ok = graphene.Boolean()
    result = graphene.Field('get_StudyPlanItemTeacherModel')
    
    def mutate(parent, info, **paramList):
        session = extractSession(info)
        result = StudyPlanItemTeacherModel(**paramList)
        session.add(result)
        session.commit()
        return create_StudyPlanItemTeacherModel(ok=True, result=result)
    pass

class update_StudyPlanItemTeacherModel(graphene.Mutation):
    class Arguments:
        id = graphene.String(required=True)    
        teacher_id = graphene.String(required=False)    
        studyplanitem_id = graphene.String(required=False)

    ok = graphene.Boolean()
    result = graphene.Field('get_StudyPlanItemTeacherModel')
    
    def mutate(parent, info, **paramList):
        session = extractSession(info)
        dbRecord = session.query(StudyPlanItemTeacherModel).filter_by(id=paramList['id']).one()
        for key, item in paramList.items():
            if key=='id':
                continue
            setattr(dbRecord, key, item)
        session.commit()
        return update_StudyPlanItemTeacherModel(ok=True, result=dbRecord)
    pass


def resolve_studyplanitem_teachers_by_id(root, info, id):
    session = extractSession(info)
    dbRecord = session.query(StudyPlanItemTeacherModel).filter_by(id=id).one()
    return dbRecord
def resolve_studyplanitem_teachers_teacher_id_starts_with(root, info, teacher_id):
    session = extractSession(info)
    dbRecords = session.query(StudyPlanItemTeacherModel).filter(StudyPlanItemTeacherModel.teacher_id.startswith(teacher_id)).all()
    return dbRecords
def resolve_studyplanitem_teachers_studyplanitem_id_starts_with(root, info, studyplanitem_id):
    session = extractSession(info)
    dbRecords = session.query(StudyPlanItemTeacherModel).filter(StudyPlanItemTeacherModel.studyplanitem_id.startswith(studyplanitem_id)).all()
    return dbRecords