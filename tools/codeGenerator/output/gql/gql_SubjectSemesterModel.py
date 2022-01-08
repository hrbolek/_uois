import graphene
from sqlalchemy.orm import relationship
from BaseModel import BaseModel

def extractSession(info):
    #return info.context['request'].scope['db_session']
    assert not info.context is None, 'Got Bad Context'
    return info.context.get('session')

class SubjectSemesterModel(BaseModel):
    __tablename__ = 'subjectsemesters'
    __table_args__ = {'extend_existing': True} 
    
    subjectmodel = relationship('SubjectModel')
    # subjectmodel = association_proxy('subjectmodel', 'keyword')
    subjecttopicmodel_collection = relationship('SubjectTopicModel')
    # subjecttopicmodel_collection = association_proxy('subjecttopicmodel_collection', 'keyword')


class get_SubjectSemesterModel(graphene.ObjectType):
    
    id = graphene.String()
    name = graphene.String()
    lastchange = graphene.DateTime()
    subject_id = graphene.String()
    
        
    subjectmodel = graphene.Field('gql_SubjectModel.get_SubjectModel')
    def resolver_subjectmodel(parent, info):
        return parent.subjectmodel
        
    subjecttopicmodel_collection = graphene.List('gql_SubjectTopicModel.get_SubjectTopicModel')
        
    def resolver_subjecttopicmodel_collection(parent, info):
        return parent.subjecttopicmodel_collection


class create_SubjectSemesterModel(graphene.Mutation):
    class Arguments:
        id = graphene.String(required=True)
        name = graphene.String(required=True)
        lastchange = graphene.DateTime(required=True)
        subject_id = graphene.String(required=True)

    ok = graphene.Boolean()
    result = graphene.Field('get_SubjectSemesterModel')
    
    def mutate(parent, info, **paramList):
        session = extractSession(info)
        result = SubjectSemesterModel(**paramList)
        session.add(result)
        session.commit()
        return create_SubjectSemesterModel(ok=True, result=result)
    pass

class update_SubjectSemesterModel(graphene.Mutation):
    class Arguments:
        id = graphene.String(required=True)    
        name = graphene.String(required=False)    
        lastchange = graphene.DateTime(required=False)    
        subject_id = graphene.String(required=False)

    ok = graphene.Boolean()
    result = graphene.Field('get_SubjectSemesterModel')
    
    def mutate(parent, info, **paramList):
        session = extractSession(info)
        dbRecord = session.query(SubjectSemesterModel).filter_by(id=paramList['id']).one()
        for key, item in paramList.items():
            if key=='id':
                continue
            setattr(dbRecord, key, item)
        session.commit()
        return update_SubjectSemesterModel(ok=True, result=dbRecord)
    pass


def resolve_subjectsemesters_by_id(root, info, id):
    session = extractSession(info)
    dbRecord = session.query(SubjectSemesterModel).filter_by(id=id).one()
    return dbRecord
def resolve_subjectsemesters_name_starts_with(root, info, name):
    session = extractSession(info)
    dbRecords = session.query(SubjectSemesterModel).filter(SubjectSemesterModel.name.startswith(name)).all()
    return dbRecords
def resolve_subjectsemesters_lastchange_starts_with(root, info, lastchange):
    session = extractSession(info)
    dbRecords = session.query(SubjectSemesterModel).filter(SubjectSemesterModel.lastchange.startswith(lastchange)).all()
    return dbRecords
def resolve_subjectsemesters_subject_id_starts_with(root, info, subject_id):
    session = extractSession(info)
    dbRecords = session.query(SubjectSemesterModel).filter(SubjectSemesterModel.subject_id.startswith(subject_id)).all()
    return dbRecords