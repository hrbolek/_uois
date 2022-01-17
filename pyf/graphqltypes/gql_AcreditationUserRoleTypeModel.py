import graphene
from sqlalchemy.orm import relationship
from BaseModel import BaseModel

def extractSession(info):
    #return info.context['request'].scope['db_session']
    assert not info.context is None, 'Got Bad Context'
    return info.context.get('session')

class AcreditationUserRoleTypeModelEx(BaseModel):
    __tablename__ = 'acreditationuserroletypes'
    __table_args__ = {'extend_existing': True} 
    
    programusermodels = relationship('ProgramUserModelEx')
    # programusermodels = association_proxy('programusermodels', 'keyword')
    subjectusermodels = relationship('SubjectUserModelEx')
    # subjectusermodels = association_proxy('subjectusermodels', 'keyword')
    subjecttopicusermodels = relationship('SubjectTopicUserModelEx')
    # subjecttopicusermodels = association_proxy('subjecttopicusermodels', 'keyword')


class AcreditationUserRoleTypeModel(graphene.ObjectType):
    
    id = graphene.String()
    name = graphene.String()
    
        
    programusermodels = graphene.List('graphqltypes.gql_ProgramUserModel.ProgramUserModel')
        
    def resolver_programusermodels(parent, info):
        return parent.programusermodels
        
    subjectusermodels = graphene.List('graphqltypes.gql_SubjectUserModel.SubjectUserModel')
        
    def resolver_subjectusermodels(parent, info):
        return parent.subjectusermodels
        
    subjecttopicusermodels = graphene.List('graphqltypes.gql_SubjectTopicUserModel.SubjectTopicUserModel')
        
    def resolver_subjecttopicusermodels(parent, info):
        return parent.subjecttopicusermodels


class create_AcreditationUserRoleTypeModel(graphene.Mutation):
    class Arguments:
        id = graphene.String(required=True)
        name = graphene.String(required=True)

    ok = graphene.Boolean()
    result = graphene.Field('graphqltypes.gql_AcreditationUserRoleTypeModel.AcreditationUserRoleTypeModel')
    
    def mutate(parent, info, **paramList):
        session = extractSession(info)
        result = AcreditationUserRoleTypeModelEx(**paramList)
        session.add(result)
        session.commit()
        return create_AcreditationUserRoleTypeModel(ok=True, result=result)
    pass

class update_AcreditationUserRoleTypeModel(graphene.Mutation):
    class Arguments:
        id = graphene.String(required=True)    
        name = graphene.String(required=False)

    ok = graphene.Boolean()
    result = graphene.Field('graphqltypes.gql_AcreditationUserRoleTypeModel.AcreditationUserRoleTypeModel')
    
    def mutate(parent, info, **paramList):
        session = extractSession(info)
        dbRecord = session.query(AcreditationUserRoleTypeModelEx).filter_by(id=paramList['id']).one()
        for key, item in paramList.items():
            if key=='id':
                continue
            setattr(dbRecord, key, item)
        session.commit()
        return update_AcreditationUserRoleTypeModel(ok=True, result=dbRecord)
    pass

def to_dict(row):
    return {column.name: getattr(row, row.__mapper__.get_property_by_column(column).key) for column in row.__table__.columns}


def resolve_acreditationuserroletypes_by_id(root, info, id):
    try:
        session = extractSession(info)
        dbRecord = session.query(AcreditationUserRoleTypeModelEx).filter_by(id=id).one()
    except Exception as e:
        print('An error occured (by_id)')
        print(e)
    print(f'to_dict(dbRecord)')
    return dbRecord
def resolve_acreditationuserroletypes_name_starts_with(root, info, name):
    try:
        session = extractSession(info)
        dbRecords = session.query(AcreditationUserRoleTypeModelEx).filter(AcreditationUserRoleTypeModel.name.startswith(name)).all()
    except Exception as e:
        print('An error occured (startswith)')
        print(e)
    return dbRecords