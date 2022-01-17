import graphene
from sqlalchemy.orm import relationship
from BaseModel import BaseModel

def extractSession(info):
    #return info.context['request'].scope['db_session']
    assert not info.context is None, 'Got Bad Context'
    return info.context.get('session')

class SubjectModelEx(BaseModel):
    __tablename__ = 'subjects'
    __table_args__ = {'extend_existing': True} 
    
    programmodel = relationship('ProgramModelEx')
    # programmodel = association_proxy('programmodel', 'keyword')
    subjectusermodels = relationship('SubjectUserModelEx')
    # subjectusermodels = association_proxy('subjectusermodels', 'keyword')
    subjectsemestermodels = relationship('SubjectSemesterModelEx')
    # subjectsemestermodels = association_proxy('subjectsemestermodels', 'keyword')


class SubjectModel(graphene.ObjectType):
    
    id = graphene.String()
    name = graphene.String()
    lastchange = graphene.DateTime()
    externalId = graphene.String()
    program_id = graphene.String()
    
        
    programmodel = graphene.Field('graphqltypes.gql_ProgramModel.ProgramModel')
    def resolver_programmodel(parent, info):
        return parent.programmodel
        
    subjectusermodels = graphene.List('graphqltypes.gql_SubjectUserModel.SubjectUserModel')
        
    def resolver_subjectusermodels(parent, info):
        return parent.subjectusermodels
        
    subjectsemestermodels = graphene.List('graphqltypes.gql_SubjectSemesterModel.SubjectSemesterModel')
        
    def resolver_subjectsemestermodels(parent, info):
        return parent.subjectsemestermodels


class create_SubjectModel(graphene.Mutation):
    class Arguments:
        id = graphene.String(required=True)
        name = graphene.String(required=True)
        lastchange = graphene.DateTime(required=True)
        externalId = graphene.String(required=True)
        program_id = graphene.String(required=True)

    ok = graphene.Boolean()
    result = graphene.Field('graphqltypes.gql_SubjectModel.SubjectModel')
    
    def mutate(parent, info, **paramList):
        session = extractSession(info)
        result = SubjectModelEx(**paramList)
        session.add(result)
        session.commit()
        return create_SubjectModel(ok=True, result=result)
    pass

class update_SubjectModel(graphene.Mutation):
    class Arguments:
        id = graphene.String(required=True)    
        name = graphene.String(required=False)    
        lastchange = graphene.DateTime(required=False)    
        externalId = graphene.String(required=False)    
        program_id = graphene.String(required=False)

    ok = graphene.Boolean()
    result = graphene.Field('graphqltypes.gql_SubjectModel.SubjectModel')
    
    def mutate(parent, info, **paramList):
        session = extractSession(info)
        dbRecord = session.query(SubjectModelEx).filter_by(id=paramList['id']).one()
        for key, item in paramList.items():
            if key=='id':
                continue
            setattr(dbRecord, key, item)
        session.commit()
        return update_SubjectModel(ok=True, result=dbRecord)
    pass

def to_dict(row):
    return {column.name: getattr(row, row.__mapper__.get_property_by_column(column).key) for column in row.__table__.columns}


def resolve_subjects_by_id(root, info, id):
    try:
        session = extractSession(info)
        dbRecord = session.query(SubjectModelEx).filter_by(id=id).one()
    except Exception as e:
        print('An error occured (by_id)')
        print(e)
    print(f'to_dict(dbRecord)')
    return dbRecord
def resolve_subjects_name_starts_with(root, info, name):
    try:
        session = extractSession(info)
        dbRecords = session.query(SubjectModelEx).filter(SubjectModel.name.startswith(name)).all()
    except Exception as e:
        print('An error occured (startswith)')
        print(e)
    return dbRecords
def resolve_subjects_lastchange_starts_with(root, info, lastchange):
    try:
        session = extractSession(info)
        dbRecords = session.query(SubjectModelEx).filter(SubjectModel.lastchange.startswith(lastchange)).all()
    except Exception as e:
        print('An error occured (startswith)')
        print(e)
    return dbRecords
def resolve_subjects_externalId_starts_with(root, info, externalId):
    try:
        session = extractSession(info)
        dbRecords = session.query(SubjectModelEx).filter(SubjectModel.externalId.startswith(externalId)).all()
    except Exception as e:
        print('An error occured (startswith)')
        print(e)
    return dbRecords
def resolve_subjects_program_id_starts_with(root, info, program_id):
    try:
        session = extractSession(info)
        dbRecords = session.query(SubjectModelEx).filter(SubjectModel.program_id.startswith(program_id)).all()
    except Exception as e:
        print('An error occured (startswith)')
        print(e)
    return dbRecords