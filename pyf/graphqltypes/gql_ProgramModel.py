import graphene
from sqlalchemy.orm import relationship
from BaseModel import BaseModel

def extractSession(info):
    #return info.context['request'].scope['db_session']
    assert not info.context is None, 'Got Bad Context'
    return info.context.get('session')

class ProgramModelEx(BaseModel):
    __tablename__ = 'programs'
    __table_args__ = {'extend_existing': True} 
    
    programusermodels = relationship('ProgramUserModelEx')
    # programusermodels = association_proxy('programusermodels', 'keyword')
    subjectmodels = relationship('SubjectModelEx')
    # subjectmodels = association_proxy('subjectmodels', 'keyword')


class ProgramModel(graphene.ObjectType):
    
    id = graphene.String()
    name = graphene.String()
    lastchange = graphene.DateTime()
    externalId = graphene.Int()
    
        
    programusermodels = graphene.List('graphqltypes.gql_ProgramUserModel.ProgramUserModel')
        
    def resolver_programusermodels(parent, info):
        return parent.programusermodels
        
    subjectmodels = graphene.List('graphqltypes.gql_SubjectModel.SubjectModel')
        
    def resolver_subjectmodels(parent, info):
        return parent.subjectmodels


class create_ProgramModel(graphene.Mutation):
    class Arguments:
        id = graphene.String(required=True)
        name = graphene.String(required=True)
        lastchange = graphene.DateTime(required=True)
        externalId = graphene.Int(required=True)

    ok = graphene.Boolean()
    result = graphene.Field('graphqltypes.gql_ProgramModel.ProgramModel')
    
    def mutate(parent, info, **paramList):
        session = extractSession(info)
        result = ProgramModelEx(**paramList)
        session.add(result)
        session.commit()
        return create_ProgramModel(ok=True, result=result)
    pass

class update_ProgramModel(graphene.Mutation):
    class Arguments:
        id = graphene.String(required=True)    
        name = graphene.String(required=False)    
        lastchange = graphene.DateTime(required=False)    
        externalId = graphene.Int(required=False)

    ok = graphene.Boolean()
    result = graphene.Field('graphqltypes.gql_ProgramModel.ProgramModel')
    
    def mutate(parent, info, **paramList):
        session = extractSession(info)
        dbRecord = session.query(ProgramModelEx).filter_by(id=paramList['id']).one()
        for key, item in paramList.items():
            if key=='id':
                continue
            setattr(dbRecord, key, item)
        session.commit()
        return update_ProgramModel(ok=True, result=dbRecord)
    pass

def to_dict(row):
    return {column.name: getattr(row, row.__mapper__.get_property_by_column(column).key) for column in row.__table__.columns}


def resolve_programs_by_id(root, info, id):
    try:
        session = extractSession(info)
        dbRecord = session.query(ProgramModelEx).filter_by(id=id).one()
    except Exception as e:
        print('An error occured (by_id)')
        print(e)
    print(f'to_dict(dbRecord)')
    return dbRecord
def resolve_programs_name_starts_with(root, info, name):
    try:
        session = extractSession(info)
        dbRecords = session.query(ProgramModelEx).filter(ProgramModel.name.startswith(name)).all()
    except Exception as e:
        print('An error occured (startswith)')
        print(e)
    return dbRecords
def resolve_programs_lastchange_starts_with(root, info, lastchange):
    try:
        session = extractSession(info)
        dbRecords = session.query(ProgramModelEx).filter(ProgramModel.lastchange.startswith(lastchange)).all()
    except Exception as e:
        print('An error occured (startswith)')
        print(e)
    return dbRecords
def resolve_programs_externalId_starts_with(root, info, externalId):
    try:
        session = extractSession(info)
        dbRecords = session.query(ProgramModelEx).filter(ProgramModel.externalId.startswith(externalId)).all()
    except Exception as e:
        print('An error occured (startswith)')
        print(e)
    return dbRecords