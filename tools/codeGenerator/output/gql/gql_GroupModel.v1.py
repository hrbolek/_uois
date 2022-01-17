import graphene
from sqlalchemy.orm import relationship
from BaseModel import BaseModel

def extractSession(info):
    #return info.context['request'].scope['db_session']
    assert not info.context is None, 'Got Bad Context'
    return info.context.get('session')

class GroupModelEx(BaseModel):
    __tablename__ = 'groups'
    __table_args__ = {'extend_existing': True} 
    
    grouptypemodel = relationship('GroupTypeModelEx')
    # grouptypemodel = association_proxy('grouptypemodel', 'keyword')
    groupconnectionmodels = relationship('GroupConnectionModelEx')
    # groupconnectionmodels = association_proxy('groupconnectionmodels', 'keyword')
    usergroupmodels = relationship('UserGroupModelEx')
    # usergroupmodels = association_proxy('usergroupmodels', 'keyword')
    rolemodels = relationship('RoleModelEx')
    # rolemodels = association_proxy('rolemodels', 'keyword')
    eventgroupmodels = relationship('EventGroupModelEx')
    # eventgroupmodels = association_proxy('eventgroupmodels', 'keyword')
    studyplangroupsmodels = relationship('StudyPlanGroupsModelEx')
    # studyplangroupsmodels = association_proxy('studyplangroupsmodels', 'keyword')
    studyplanitemgroupmodels = relationship('StudyPlanItemGroupModelEx')
    # studyplanitemgroupmodels = association_proxy('studyplanitemgroupmodels', 'keyword')


class GroupModel(graphene.ObjectType):
    
    id = graphene.String()
    name = graphene.String()
    abbreviation = graphene.String()
    lastchange = graphene.DateTime()
    entryYearId = graphene.Int()
    externalId = graphene.String()
    UIC = graphene.String()
    grouptype_id = graphene.String()
    
        
    grouptypemodel = graphene.Field('graphqltypes.gql_GroupTypeModel.GroupTypeModel')
    def resolver_grouptypemodel(parent, info):
        return parent.grouptypemodel
        
    groupconnectionmodels = graphene.List('graphqltypes.gql_GroupConnectionModel.GroupConnectionModel')
        
    def resolver_groupconnectionmodels(parent, info):
        return parent.groupconnectionmodels
        
    usergroupmodels = graphene.List('graphqltypes.gql_UserGroupModel.UserGroupModel')
        
    def resolver_usergroupmodels(parent, info):
        return parent.usergroupmodels
        
    rolemodels = graphene.List('graphqltypes.gql_RoleModel.RoleModel')
        
    def resolver_rolemodels(parent, info):
        return parent.rolemodels
        
    eventgroupmodels = graphene.List('graphqltypes.gql_EventGroupModel.EventGroupModel')
        
    def resolver_eventgroupmodels(parent, info):
        return parent.eventgroupmodels
        
    studyplangroupsmodels = graphene.List('graphqltypes.gql_StudyPlanGroupsModel.StudyPlanGroupsModel')
        
    def resolver_studyplangroupsmodels(parent, info):
        return parent.studyplangroupsmodels
        
    studyplanitemgroupmodels = graphene.List('graphqltypes.gql_StudyPlanItemGroupModel.StudyPlanItemGroupModel')
        
    def resolver_studyplanitemgroupmodels(parent, info):
        return parent.studyplanitemgroupmodels


class create_GroupModel(graphene.Mutation):
    class Arguments:
        id = graphene.String(required=True)
        name = graphene.String(required=True)
        abbreviation = graphene.String(required=True)
        lastchange = graphene.DateTime(required=True)
        entryYearId = graphene.Int(required=True)
        externalId = graphene.String(required=True)
        UIC = graphene.String(required=True)
        grouptype_id = graphene.String(required=True)

    ok = graphene.Boolean()
    result = graphene.Field('graphqltypes.gql_GroupModel.GroupModel')
    
    def mutate(parent, info, **paramList):
        session = extractSession(info)
        result = GroupModelEx(**paramList)
        session.add(result)
        session.commit()
        return create_GroupModel(ok=True, result=result)
    pass

class update_GroupModel(graphene.Mutation):
    class Arguments:
        id = graphene.String(required=True)    
        name = graphene.String(required=False)    
        abbreviation = graphene.String(required=False)    
        lastchange = graphene.DateTime(required=False)    
        entryYearId = graphene.Int(required=False)    
        externalId = graphene.String(required=False)    
        UIC = graphene.String(required=False)    
        grouptype_id = graphene.String(required=False)

    ok = graphene.Boolean()
    result = graphene.Field('graphqltypes.gql_GroupModel.GroupModel')
    
    def mutate(parent, info, **paramList):
        session = extractSession(info)
        dbRecord = session.query(GroupModelEx).filter_by(id=paramList['id']).one()
        for key, item in paramList.items():
            if key=='id':
                continue
            setattr(dbRecord, key, item)
        session.commit()
        return update_GroupModel(ok=True, result=dbRecord)
    pass

def to_dict(row):
    return {column.name: getattr(row, row.__mapper__.get_property_by_column(column).key) for column in row.__table__.columns}


def resolve_groups_by_id(root, info, id):
    try:
        session = extractSession(info)
        dbRecord = session.query(GroupModelEx).filter_by(id=id).one()
    except Exception as e:
        print('An error occured (by_id)')
        print(e)
    print(f'to_dict(dbRecord)')
    return dbRecord
def resolve_groups_name_starts_with(root, info, name):
    try:
        session = extractSession(info)
        dbRecords = session.query(GroupModelEx).filter(GroupModel.name.startswith(name)).all()
    except Exception as e:
        print('An error occured (startswith)')
        print(e)
    return dbRecords
def resolve_groups_abbreviation_starts_with(root, info, abbreviation):
    try:
        session = extractSession(info)
        dbRecords = session.query(GroupModelEx).filter(GroupModel.abbreviation.startswith(abbreviation)).all()
    except Exception as e:
        print('An error occured (startswith)')
        print(e)
    return dbRecords
def resolve_groups_lastchange_starts_with(root, info, lastchange):
    try:
        session = extractSession(info)
        dbRecords = session.query(GroupModelEx).filter(GroupModel.lastchange.startswith(lastchange)).all()
    except Exception as e:
        print('An error occured (startswith)')
        print(e)
    return dbRecords
def resolve_groups_entryYearId_starts_with(root, info, entryYearId):
    try:
        session = extractSession(info)
        dbRecords = session.query(GroupModelEx).filter(GroupModel.entryYearId.startswith(entryYearId)).all()
    except Exception as e:
        print('An error occured (startswith)')
        print(e)
    return dbRecords
def resolve_groups_externalId_starts_with(root, info, externalId):
    try:
        session = extractSession(info)
        dbRecords = session.query(GroupModelEx).filter(GroupModel.externalId.startswith(externalId)).all()
    except Exception as e:
        print('An error occured (startswith)')
        print(e)
    return dbRecords
def resolve_groups_UIC_starts_with(root, info, UIC):
    try:
        session = extractSession(info)
        dbRecords = session.query(GroupModelEx).filter(GroupModel.UIC.startswith(UIC)).all()
    except Exception as e:
        print('An error occured (startswith)')
        print(e)
    return dbRecords
def resolve_groups_grouptype_id_starts_with(root, info, grouptype_id):
    try:
        session = extractSession(info)
        dbRecords = session.query(GroupModelEx).filter(GroupModel.grouptype_id.startswith(grouptype_id)).all()
    except Exception as e:
        print('An error occured (startswith)')
        print(e)
    return dbRecords