import graphene
from sqlalchemy.orm import relationship
from BaseModel import BaseModel

def extractSession(info):
    #return info.context['request'].scope['db_session']
    assert not info.context is None, 'Got Bad Context'
    return info.context.get('session')

class SubjectSemesterModelEx(BaseModel):
    __tablename__ = 'subjectsemesters'
    __table_args__ = {'extend_existing': True} 
    
    subjectmodel = relationship('SubjectModelEx')
    # subjectmodel = association_proxy('subjectmodel', 'keyword')
    subjecttopicmodels = relationship('SubjectTopicModelEx')
    # subjecttopicmodels = association_proxy('subjecttopicmodels', 'keyword')


class SubjectSemesterModel(graphene.ObjectType):
    
    id = graphene.String()
    name = graphene.String()
    lastchange = graphene.DateTime()
    subject_id = graphene.String()
    
        
    subjectmodel = graphene.Field('graphqltypes.gql_SubjectModel.SubjectModel')
    def resolver_subjectmodel(parent, info):
        return parent.subjectmodel
        
    subjecttopicmodels = graphene.List('graphqltypes.gql_SubjectTopicModel.SubjectTopicModel')
        
    def resolver_subjecttopicmodels(parent, info):
        return parent.subjecttopicmodels


class create_SubjectSemesterModel(graphene.Mutation):
    class Arguments:
        id = graphene.String(required=True)
        name = graphene.String(required=True)
        lastchange = graphene.DateTime(required=True)
        subject_id = graphene.String(required=True)

    ok = graphene.Boolean()
    result = graphene.Field('graphqltypes.gql_SubjectSemesterModel.SubjectSemesterModel')
    
    def mutate(parent, info, **paramList):
        session = extractSession(info)
        result = SubjectSemesterModelEx(**paramList)
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
    result = graphene.Field('graphqltypes.gql_SubjectSemesterModel.SubjectSemesterModel')
    
    def mutate(parent, info, **paramList):
        session = extractSession(info)
        dbRecord = session.query(SubjectSemesterModelEx).filter_by(id=paramList['id']).one()
        for key, item in paramList.items():
            if key=='id':
                continue
            setattr(dbRecord, key, item)
        session.commit()
        return update_SubjectSemesterModel(ok=True, result=dbRecord)
    pass

def to_dict(row):
    return {column.name: getattr(row, row.__mapper__.get_property_by_column(column).key) for column in row.__table__.columns}


def resolve_subjectsemesters_by_id(root, info, id):
    try:
        session = extractSession(info)
        dbRecord = session.query(SubjectSemesterModelEx).filter_by(id=id).one()
    except Exception as e:
        print('An error occured (by_id)')
        print(e)
    print(f'to_dict(dbRecord)')
    return dbRecord
def resolve_subjectsemesters_name_starts_with(root, info, name):
    try:
        session = extractSession(info)
        dbRecords = session.query(SubjectSemesterModelEx).filter(SubjectSemesterModel.name.startswith(name)).all()
    except Exception as e:
        print('An error occured (startswith)')
        print(e)
    return dbRecords
def resolve_subjectsemesters_lastchange_starts_with(root, info, lastchange):
    try:
        session = extractSession(info)
        dbRecords = session.query(SubjectSemesterModelEx).filter(SubjectSemesterModel.lastchange.startswith(lastchange)).all()
    except Exception as e:
        print('An error occured (startswith)')
        print(e)
    return dbRecords
def resolve_subjectsemesters_subject_id_starts_with(root, info, subject_id):
    try:
        session = extractSession(info)
        dbRecords = session.query(SubjectSemesterModelEx).filter(SubjectSemesterModel.subject_id.startswith(subject_id)).all()
    except Exception as e:
        print('An error occured (startswith)')
        print(e)
    return dbRecords