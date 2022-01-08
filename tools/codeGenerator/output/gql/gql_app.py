import graphene
from contextlib import contextmanager


import gql_AcreditationUserRoleTypeModel
import gql_ArealModel
import gql_BuildingModel
import gql_EventGroupModel
import gql_EventModel
import gql_EventRoomModel
import gql_EventUserModel
import gql_GroupConnectionModel
import gql_GroupModel
import gql_GroupTypeModel
import gql_ProgramModel
import gql_ProgramUserModel
import gql_RoleModel
import gql_RoleTypeModel
import gql_RoomModel
import gql_StudyPlanGroupsModel
import gql_StudyPlanItemEventModel
import gql_StudyPlanItemGroupModel
import gql_StudyPlanItemModel
import gql_StudyPlanItemTeacherModel
import gql_StudyPlanModel
import gql_SubjectModel
import gql_SubjectSemesterModel
import gql_SubjectTopicModel
import gql_SubjectTopicUserModel
import gql_SubjectUserModel
import gql_UserGroupModel
import gql_UserModel

class query(graphene.ObjectType):

    #{'SQLTableName': 'acreditationuserroletypes', 'locals': {'id': {'name': 'id', 'type': 'graphene.String', 'column': 'id', 'isPrimaryKey': True}, 'name': {'name': 'name', 'type': 'graphene.String', 'column': 'name', 'isPrimaryKey': False}}, 'relations': {'programusermodel_collection': {'name': 'programusermodel_collection', 'useList': True, 'type': 'ProgramUserModel'}, 'subjectusermodel_collection': {'name': 'subjectusermodel_collection', 'useList': True, 'type': 'SubjectUserModel'}, 'subjecttopicusermodel_collection': {'name': 'subjecttopicusermodel_collection', 'useList': True, 'type': 'SubjectTopicUserModel'}}}
    #{'name': 'id', 'type': 'graphene.String', 'column': 'id', 'isPrimaryKey': True}
    acreditationuserroletypes_by_id =  graphene.Field(
        'gql_AcreditationUserRoleTypeModel.get_AcreditationUserRoleTypeModel', 
        id=graphene.String(required=True),
        resolver=gql_AcreditationUserRoleTypeModel.resolve_AcreditationUserRoleTypeModel_by_id
    )
    #{'name': 'name', 'type': 'graphene.String', 'column': 'name', 'isPrimaryKey': False}
    acreditationuserroletypes_name_starts_with =  graphene.Field(
        'gql_AcreditationUserRoleTypeModel.get_AcreditationUserRoleTypeModel', 
        name=graphene.String(required=True),
        resolver=gql_AcreditationUserRoleTypeModel.resolve_AcreditationUserRoleTypeModel_by_name
    )
    #{'SQLTableName': 'areals', 'locals': {'id': {'name': 'id', 'type': 'graphene.String', 'column': 'id', 'isPrimaryKey': True}, 'name': {'name': 'name', 'type': 'graphene.String', 'column': 'name', 'isPrimaryKey': False}, 'externalId': {'name': 'externalId', 'type': 'graphene.String', 'column': 'externalId', 'isPrimaryKey': False}, 'lastchange': {'name': 'lastchange', 'type': 'graphene.DateTime', 'column': 'lastchange', 'isPrimaryKey': False}}, 'relations': {'buildingmodel_collection': {'name': 'buildingmodel_collection', 'useList': True, 'type': 'BuildingModel'}}}
    #{'name': 'id', 'type': 'graphene.String', 'column': 'id', 'isPrimaryKey': True}
    areals_by_id =  graphene.Field(
        'gql_ArealModel.get_ArealModel', 
        id=graphene.String(required=True),
        resolver=gql_ArealModel.resolve_ArealModel_by_id
    )
    #{'name': 'name', 'type': 'graphene.String', 'column': 'name', 'isPrimaryKey': False}
    areals_name_starts_with =  graphene.Field(
        'gql_ArealModel.get_ArealModel', 
        name=graphene.String(required=True),
        resolver=gql_ArealModel.resolve_ArealModel_by_name
    )
    #{'name': 'externalId', 'type': 'graphene.String', 'column': 'externalId', 'isPrimaryKey': False}
    areals_externalId_starts_with =  graphene.Field(
        'gql_ArealModel.get_ArealModel', 
        externalId=graphene.String(required=True),
        resolver=gql_ArealModel.resolve_ArealModel_by_externalId
    )
    #{'name': 'lastchange', 'type': 'graphene.DateTime', 'column': 'lastchange', 'isPrimaryKey': False}
    areals_lastchange_starts_with =  graphene.Field(
        'gql_ArealModel.get_ArealModel', 
        lastchange=graphene.String(required=True),
        resolver=gql_ArealModel.resolve_ArealModel_by_lastchange
    )
    #{'SQLTableName': 'buildings', 'locals': {'id': {'name': 'id', 'type': 'graphene.String', 'column': 'id', 'isPrimaryKey': True}, 'name': {'name': 'name', 'type': 'graphene.String', 'column': 'name', 'isPrimaryKey': False}, 'lastchange': {'name': 'lastchange', 'type': 'graphene.DateTime', 'column': 'lastchange', 'isPrimaryKey': False}, 'externalId': {'name': 'externalId', 'type': 'graphene.String', 'column': 'externalId', 'isPrimaryKey': False}, 'areal_id': {'name': 'areal_id', 'type': 'graphene.String', 'column': 'areal_id', 'isPrimaryKey': False}}, 'relations': {'arealmodel': {'name': 'arealmodel', 'useList': False, 'type': 'ArealModel'}, 'roommodel_collection': {'name': 'roommodel_collection', 'useList': True, 'type': 'RoomModel'}}}
    #{'name': 'id', 'type': 'graphene.String', 'column': 'id', 'isPrimaryKey': True}
    buildings_by_id =  graphene.Field(
        'gql_BuildingModel.get_BuildingModel', 
        id=graphene.String(required=True),
        resolver=gql_BuildingModel.resolve_BuildingModel_by_id
    )
    #{'name': 'name', 'type': 'graphene.String', 'column': 'name', 'isPrimaryKey': False}
    buildings_name_starts_with =  graphene.Field(
        'gql_BuildingModel.get_BuildingModel', 
        name=graphene.String(required=True),
        resolver=gql_BuildingModel.resolve_BuildingModel_by_name
    )
    #{'name': 'lastchange', 'type': 'graphene.DateTime', 'column': 'lastchange', 'isPrimaryKey': False}
    buildings_lastchange_starts_with =  graphene.Field(
        'gql_BuildingModel.get_BuildingModel', 
        lastchange=graphene.String(required=True),
        resolver=gql_BuildingModel.resolve_BuildingModel_by_lastchange
    )
    #{'name': 'externalId', 'type': 'graphene.String', 'column': 'externalId', 'isPrimaryKey': False}
    buildings_externalId_starts_with =  graphene.Field(
        'gql_BuildingModel.get_BuildingModel', 
        externalId=graphene.String(required=True),
        resolver=gql_BuildingModel.resolve_BuildingModel_by_externalId
    )
    #{'name': 'areal_id', 'type': 'graphene.String', 'column': 'areal_id', 'isPrimaryKey': False}
    buildings_areal_id_starts_with =  graphene.Field(
        'gql_BuildingModel.get_BuildingModel', 
        areal_id=graphene.String(required=True),
        resolver=gql_BuildingModel.resolve_BuildingModel_by_areal_id
    )
    #{'SQLTableName': 'events_groups', 'locals': {'id': {'name': 'id', 'type': 'graphene.String', 'column': 'id', 'isPrimaryKey': True}, 'group_id': {'name': 'group_id', 'type': 'graphene.String', 'column': 'group_id', 'isPrimaryKey': False}, 'event_id': {'name': 'event_id', 'type': 'graphene.String', 'column': 'event_id', 'isPrimaryKey': False}}, 'relations': {'eventmodel': {'name': 'eventmodel', 'useList': False, 'type': 'EventModel'}, 'groupmodel': {'name': 'groupmodel', 'useList': False, 'type': 'GroupModel'}}}
    #{'name': 'id', 'type': 'graphene.String', 'column': 'id', 'isPrimaryKey': True}
    events_groups_by_id =  graphene.Field(
        'gql_EventGroupModel.get_EventGroupModel', 
        id=graphene.String(required=True),
        resolver=gql_EventGroupModel.resolve_EventGroupModel_by_id
    )
    #{'name': 'group_id', 'type': 'graphene.String', 'column': 'group_id', 'isPrimaryKey': False}
    events_groups_group_id_starts_with =  graphene.Field(
        'gql_EventGroupModel.get_EventGroupModel', 
        group_id=graphene.String(required=True),
        resolver=gql_EventGroupModel.resolve_EventGroupModel_by_group_id
    )
    #{'name': 'event_id', 'type': 'graphene.String', 'column': 'event_id', 'isPrimaryKey': False}
    events_groups_event_id_starts_with =  graphene.Field(
        'gql_EventGroupModel.get_EventGroupModel', 
        event_id=graphene.String(required=True),
        resolver=gql_EventGroupModel.resolve_EventGroupModel_by_event_id
    )
    #{'SQLTableName': 'events', 'locals': {'id': {'name': 'id', 'type': 'graphene.String', 'column': 'id', 'isPrimaryKey': True}, 'start': {'name': 'start', 'type': 'graphene.DateTime', 'column': 'start', 'isPrimaryKey': False}, 'end': {'name': 'end', 'type': 'graphene.DateTime', 'column': 'end', 'isPrimaryKey': False}, 'label': {'name': 'label', 'type': 'graphene.String', 'column': 'label', 'isPrimaryKey': False}, 'externalId': {'name': 'externalId', 'type': 'graphene.String', 'column': 'externalId', 'isPrimaryKey': False}, 'lastchange': {'name': 'lastchange', 'type': 'graphene.DateTime', 'column': 'lastchange', 'isPrimaryKey': False}}, 'relations': {'eventusermodel_collection': {'name': 'eventusermodel_collection', 'useList': True, 'type': 'EventUserModel'}, 'eventgroupmodel_collection': {'name': 'eventgroupmodel_collection', 'useList': True, 'type': 'EventGroupModel'}, 'studyplanitemeventmodel_collection': {'name': 'studyplanitemeventmodel_collection', 'useList': True, 'type': 'StudyPlanItemEventModel'}, 'eventroommodel_collection': {'name': 'eventroommodel_collection', 'useList': True, 'type': 'EventRoomModel'}}}
    #{'name': 'id', 'type': 'graphene.String', 'column': 'id', 'isPrimaryKey': True}
    events_by_id =  graphene.Field(
        'gql_EventModel.get_EventModel', 
        id=graphene.String(required=True),
        resolver=gql_EventModel.resolve_EventModel_by_id
    )
    #{'name': 'start', 'type': 'graphene.DateTime', 'column': 'start', 'isPrimaryKey': False}
    events_start_starts_with =  graphene.Field(
        'gql_EventModel.get_EventModel', 
        start=graphene.String(required=True),
        resolver=gql_EventModel.resolve_EventModel_by_start
    )
    #{'name': 'end', 'type': 'graphene.DateTime', 'column': 'end', 'isPrimaryKey': False}
    events_end_starts_with =  graphene.Field(
        'gql_EventModel.get_EventModel', 
        end=graphene.String(required=True),
        resolver=gql_EventModel.resolve_EventModel_by_end
    )
    #{'name': 'label', 'type': 'graphene.String', 'column': 'label', 'isPrimaryKey': False}
    events_label_starts_with =  graphene.Field(
        'gql_EventModel.get_EventModel', 
        label=graphene.String(required=True),
        resolver=gql_EventModel.resolve_EventModel_by_label
    )
    #{'name': 'externalId', 'type': 'graphene.String', 'column': 'externalId', 'isPrimaryKey': False}
    events_externalId_starts_with =  graphene.Field(
        'gql_EventModel.get_EventModel', 
        externalId=graphene.String(required=True),
        resolver=gql_EventModel.resolve_EventModel_by_externalId
    )
    #{'name': 'lastchange', 'type': 'graphene.DateTime', 'column': 'lastchange', 'isPrimaryKey': False}
    events_lastchange_starts_with =  graphene.Field(
        'gql_EventModel.get_EventModel', 
        lastchange=graphene.String(required=True),
        resolver=gql_EventModel.resolve_EventModel_by_lastchange
    )
    #{'SQLTableName': 'events_rooms', 'locals': {'id': {'name': 'id', 'type': 'graphene.String', 'column': 'id', 'isPrimaryKey': True}, 'room_id': {'name': 'room_id', 'type': 'graphene.String', 'column': 'room_id', 'isPrimaryKey': False}, 'event_id': {'name': 'event_id', 'type': 'graphene.String', 'column': 'event_id', 'isPrimaryKey': False}}, 'relations': {'roommodel': {'name': 'roommodel', 'useList': False, 'type': 'RoomModel'}, 'eventmodel': {'name': 'eventmodel', 'useList': False, 'type': 'EventModel'}}}
    #{'name': 'id', 'type': 'graphene.String', 'column': 'id', 'isPrimaryKey': True}
    events_rooms_by_id =  graphene.Field(
        'gql_EventRoomModel.get_EventRoomModel', 
        id=graphene.String(required=True),
        resolver=gql_EventRoomModel.resolve_EventRoomModel_by_id
    )
    #{'name': 'room_id', 'type': 'graphene.String', 'column': 'room_id', 'isPrimaryKey': False}
    events_rooms_room_id_starts_with =  graphene.Field(
        'gql_EventRoomModel.get_EventRoomModel', 
        room_id=graphene.String(required=True),
        resolver=gql_EventRoomModel.resolve_EventRoomModel_by_room_id
    )
    #{'name': 'event_id', 'type': 'graphene.String', 'column': 'event_id', 'isPrimaryKey': False}
    events_rooms_event_id_starts_with =  graphene.Field(
        'gql_EventRoomModel.get_EventRoomModel', 
        event_id=graphene.String(required=True),
        resolver=gql_EventRoomModel.resolve_EventRoomModel_by_event_id
    )
    #{'SQLTableName': 'events_users', 'locals': {'id': {'name': 'id', 'type': 'graphene.String', 'column': 'id', 'isPrimaryKey': True}, 'user_id': {'name': 'user_id', 'type': 'graphene.String', 'column': 'user_id', 'isPrimaryKey': False}, 'event_id': {'name': 'event_id', 'type': 'graphene.String', 'column': 'event_id', 'isPrimaryKey': False}}, 'relations': {'usermodel': {'name': 'usermodel', 'useList': False, 'type': 'UserModel'}, 'eventmodel': {'name': 'eventmodel', 'useList': False, 'type': 'EventModel'}}}
    #{'name': 'id', 'type': 'graphene.String', 'column': 'id', 'isPrimaryKey': True}
    events_users_by_id =  graphene.Field(
        'gql_EventUserModel.get_EventUserModel', 
        id=graphene.String(required=True),
        resolver=gql_EventUserModel.resolve_EventUserModel_by_id
    )
    #{'name': 'user_id', 'type': 'graphene.String', 'column': 'user_id', 'isPrimaryKey': False}
    events_users_user_id_starts_with =  graphene.Field(
        'gql_EventUserModel.get_EventUserModel', 
        user_id=graphene.String(required=True),
        resolver=gql_EventUserModel.resolve_EventUserModel_by_user_id
    )
    #{'name': 'event_id', 'type': 'graphene.String', 'column': 'event_id', 'isPrimaryKey': False}
    events_users_event_id_starts_with =  graphene.Field(
        'gql_EventUserModel.get_EventUserModel', 
        event_id=graphene.String(required=True),
        resolver=gql_EventUserModel.resolve_EventUserModel_by_event_id
    )
    #{'SQLTableName': 'groups_groups', 'locals': {'id': {'name': 'id', 'type': 'graphene.String', 'column': 'id', 'isPrimaryKey': True}, 'child_id': {'name': 'child_id', 'type': 'graphene.String', 'column': 'child_id', 'isPrimaryKey': False}, 'parent_id': {'name': 'parent_id', 'type': 'graphene.String', 'column': 'parent_id', 'isPrimaryKey': False}}, 'relations': {'groupmodel': {'name': 'groupmodel', 'useList': False, 'type': 'GroupModel'}}}
    #{'name': 'id', 'type': 'graphene.String', 'column': 'id', 'isPrimaryKey': True}
    groups_groups_by_id =  graphene.Field(
        'gql_GroupConnectionModel.get_GroupConnectionModel', 
        id=graphene.String(required=True),
        resolver=gql_GroupConnectionModel.resolve_GroupConnectionModel_by_id
    )
    #{'name': 'child_id', 'type': 'graphene.String', 'column': 'child_id', 'isPrimaryKey': False}
    groups_groups_child_id_starts_with =  graphene.Field(
        'gql_GroupConnectionModel.get_GroupConnectionModel', 
        child_id=graphene.String(required=True),
        resolver=gql_GroupConnectionModel.resolve_GroupConnectionModel_by_child_id
    )
    #{'name': 'parent_id', 'type': 'graphene.String', 'column': 'parent_id', 'isPrimaryKey': False}
    groups_groups_parent_id_starts_with =  graphene.Field(
        'gql_GroupConnectionModel.get_GroupConnectionModel', 
        parent_id=graphene.String(required=True),
        resolver=gql_GroupConnectionModel.resolve_GroupConnectionModel_by_parent_id
    )
    #{'SQLTableName': 'groups', 'locals': {'id': {'name': 'id', 'type': 'graphene.String', 'column': 'id', 'isPrimaryKey': True}, 'name': {'name': 'name', 'type': 'graphene.String', 'column': 'name', 'isPrimaryKey': False}, 'abbreviation': {'name': 'abbreviation', 'type': 'graphene.String', 'column': 'abbreviation', 'isPrimaryKey': False}, 'lastchange': {'name': 'lastchange', 'type': 'graphene.DateTime', 'column': 'lastchange', 'isPrimaryKey': False}, 'entryYearId': {'name': 'entryYearId', 'type': 'graphene.Int', 'column': 'entryYearId', 'isPrimaryKey': False}, 'externalId': {'name': 'externalId', 'type': 'graphene.String', 'column': 'externalId', 'isPrimaryKey': False}, 'UIC': {'name': 'UIC', 'type': 'graphene.String', 'column': 'UIC', 'isPrimaryKey': False}, 'grouptype_id': {'name': 'grouptype_id', 'type': 'graphene.String', 'column': 'grouptype_id', 'isPrimaryKey': False}}, 'relations': {'grouptypemodel': {'name': 'grouptypemodel', 'useList': False, 'type': 'GroupTypeModel'}, 'groupconnectionmodel_collection': {'name': 'groupconnectionmodel_collection', 'useList': True, 'type': 'GroupConnectionModel'}, 'usergroupmodel_collection': {'name': 'usergroupmodel_collection', 'useList': True, 'type': 'UserGroupModel'}, 'rolemodel_collection': {'name': 'rolemodel_collection', 'useList': True, 'type': 'RoleModel'}, 'eventgroupmodel_collection': {'name': 'eventgroupmodel_collection', 'useList': True, 'type': 'EventGroupModel'}, 'studyplangroupsmodel_collection': {'name': 'studyplangroupsmodel_collection', 'useList': True, 'type': 'StudyPlanGroupsModel'}, 'studyplanitemgroupmodel_collection': {'name': 'studyplanitemgroupmodel_collection', 'useList': True, 'type': 'StudyPlanItemGroupModel'}}}
    #{'name': 'id', 'type': 'graphene.String', 'column': 'id', 'isPrimaryKey': True}
    groups_by_id =  graphene.Field(
        'gql_GroupModel.get_GroupModel', 
        id=graphene.String(required=True),
        resolver=gql_GroupModel.resolve_GroupModel_by_id
    )
    #{'name': 'name', 'type': 'graphene.String', 'column': 'name', 'isPrimaryKey': False}
    groups_name_starts_with =  graphene.Field(
        'gql_GroupModel.get_GroupModel', 
        name=graphene.String(required=True),
        resolver=gql_GroupModel.resolve_GroupModel_by_name
    )
    #{'name': 'abbreviation', 'type': 'graphene.String', 'column': 'abbreviation', 'isPrimaryKey': False}
    groups_abbreviation_starts_with =  graphene.Field(
        'gql_GroupModel.get_GroupModel', 
        abbreviation=graphene.String(required=True),
        resolver=gql_GroupModel.resolve_GroupModel_by_abbreviation
    )
    #{'name': 'lastchange', 'type': 'graphene.DateTime', 'column': 'lastchange', 'isPrimaryKey': False}
    groups_lastchange_starts_with =  graphene.Field(
        'gql_GroupModel.get_GroupModel', 
        lastchange=graphene.String(required=True),
        resolver=gql_GroupModel.resolve_GroupModel_by_lastchange
    )
    #{'name': 'entryYearId', 'type': 'graphene.Int', 'column': 'entryYearId', 'isPrimaryKey': False}
    groups_entryYearId_starts_with =  graphene.Field(
        'gql_GroupModel.get_GroupModel', 
        entryYearId=graphene.String(required=True),
        resolver=gql_GroupModel.resolve_GroupModel_by_entryYearId
    )
    #{'name': 'externalId', 'type': 'graphene.String', 'column': 'externalId', 'isPrimaryKey': False}
    groups_externalId_starts_with =  graphene.Field(
        'gql_GroupModel.get_GroupModel', 
        externalId=graphene.String(required=True),
        resolver=gql_GroupModel.resolve_GroupModel_by_externalId
    )
    #{'name': 'UIC', 'type': 'graphene.String', 'column': 'UIC', 'isPrimaryKey': False}
    groups_UIC_starts_with =  graphene.Field(
        'gql_GroupModel.get_GroupModel', 
        UIC=graphene.String(required=True),
        resolver=gql_GroupModel.resolve_GroupModel_by_UIC
    )
    #{'name': 'grouptype_id', 'type': 'graphene.String', 'column': 'grouptype_id', 'isPrimaryKey': False}
    groups_grouptype_id_starts_with =  graphene.Field(
        'gql_GroupModel.get_GroupModel', 
        grouptype_id=graphene.String(required=True),
        resolver=gql_GroupModel.resolve_GroupModel_by_grouptype_id
    )
    #{'SQLTableName': 'grouptypes', 'locals': {'id': {'name': 'id', 'type': 'graphene.String', 'column': 'id', 'isPrimaryKey': True}, 'name': {'name': 'name', 'type': 'graphene.String', 'column': 'name', 'isPrimaryKey': False}}, 'relations': {'groupmodel_collection': {'name': 'groupmodel_collection', 'useList': True, 'type': 'GroupModel'}}}
    #{'name': 'id', 'type': 'graphene.String', 'column': 'id', 'isPrimaryKey': True}
    grouptypes_by_id =  graphene.Field(
        'gql_GroupTypeModel.get_GroupTypeModel', 
        id=graphene.String(required=True),
        resolver=gql_GroupTypeModel.resolve_GroupTypeModel_by_id
    )
    #{'name': 'name', 'type': 'graphene.String', 'column': 'name', 'isPrimaryKey': False}
    grouptypes_name_starts_with =  graphene.Field(
        'gql_GroupTypeModel.get_GroupTypeModel', 
        name=graphene.String(required=True),
        resolver=gql_GroupTypeModel.resolve_GroupTypeModel_by_name
    )
    #{'SQLTableName': 'programs', 'locals': {'id': {'name': 'id', 'type': 'graphene.String', 'column': 'id', 'isPrimaryKey': True}, 'name': {'name': 'name', 'type': 'graphene.String', 'column': 'name', 'isPrimaryKey': False}, 'lastchange': {'name': 'lastchange', 'type': 'graphene.DateTime', 'column': 'lastchange', 'isPrimaryKey': False}, 'externalId': {'name': 'externalId', 'type': 'graphene.Int', 'column': 'externalId', 'isPrimaryKey': False}}, 'relations': {'programusermodel_collection': {'name': 'programusermodel_collection', 'useList': True, 'type': 'ProgramUserModel'}, 'subjectmodel_collection': {'name': 'subjectmodel_collection', 'useList': True, 'type': 'SubjectModel'}}}
    #{'name': 'id', 'type': 'graphene.String', 'column': 'id', 'isPrimaryKey': True}
    programs_by_id =  graphene.Field(
        'gql_ProgramModel.get_ProgramModel', 
        id=graphene.String(required=True),
        resolver=gql_ProgramModel.resolve_ProgramModel_by_id
    )
    #{'name': 'name', 'type': 'graphene.String', 'column': 'name', 'isPrimaryKey': False}
    programs_name_starts_with =  graphene.Field(
        'gql_ProgramModel.get_ProgramModel', 
        name=graphene.String(required=True),
        resolver=gql_ProgramModel.resolve_ProgramModel_by_name
    )
    #{'name': 'lastchange', 'type': 'graphene.DateTime', 'column': 'lastchange', 'isPrimaryKey': False}
    programs_lastchange_starts_with =  graphene.Field(
        'gql_ProgramModel.get_ProgramModel', 
        lastchange=graphene.String(required=True),
        resolver=gql_ProgramModel.resolve_ProgramModel_by_lastchange
    )
    #{'name': 'externalId', 'type': 'graphene.Int', 'column': 'externalId', 'isPrimaryKey': False}
    programs_externalId_starts_with =  graphene.Field(
        'gql_ProgramModel.get_ProgramModel', 
        externalId=graphene.String(required=True),
        resolver=gql_ProgramModel.resolve_ProgramModel_by_externalId
    )
    #{'SQLTableName': 'programs_users', 'locals': {'id': {'name': 'id', 'type': 'graphene.String', 'column': 'id', 'isPrimaryKey': True}, 'program_id': {'name': 'program_id', 'type': 'graphene.String', 'column': 'program_id', 'isPrimaryKey': False}, 'user_id': {'name': 'user_id', 'type': 'graphene.String', 'column': 'user_id', 'isPrimaryKey': False}, 'roletype_id': {'name': 'roletype_id', 'type': 'graphene.String', 'column': 'roletype_id', 'isPrimaryKey': False}}, 'relations': {'acreditationuserroletypemodel': {'name': 'acreditationuserroletypemodel', 'useList': False, 'type': 'AcreditationUserRoleTypeModel'}, 'programmodel': {'name': 'programmodel', 'useList': False, 'type': 'ProgramModel'}, 'usermodel': {'name': 'usermodel', 'useList': False, 'type': 'UserModel'}}}
    #{'name': 'id', 'type': 'graphene.String', 'column': 'id', 'isPrimaryKey': True}
    programs_users_by_id =  graphene.Field(
        'gql_ProgramUserModel.get_ProgramUserModel', 
        id=graphene.String(required=True),
        resolver=gql_ProgramUserModel.resolve_ProgramUserModel_by_id
    )
    #{'name': 'program_id', 'type': 'graphene.String', 'column': 'program_id', 'isPrimaryKey': False}
    programs_users_program_id_starts_with =  graphene.Field(
        'gql_ProgramUserModel.get_ProgramUserModel', 
        program_id=graphene.String(required=True),
        resolver=gql_ProgramUserModel.resolve_ProgramUserModel_by_program_id
    )
    #{'name': 'user_id', 'type': 'graphene.String', 'column': 'user_id', 'isPrimaryKey': False}
    programs_users_user_id_starts_with =  graphene.Field(
        'gql_ProgramUserModel.get_ProgramUserModel', 
        user_id=graphene.String(required=True),
        resolver=gql_ProgramUserModel.resolve_ProgramUserModel_by_user_id
    )
    #{'name': 'roletype_id', 'type': 'graphene.String', 'column': 'roletype_id', 'isPrimaryKey': False}
    programs_users_roletype_id_starts_with =  graphene.Field(
        'gql_ProgramUserModel.get_ProgramUserModel', 
        roletype_id=graphene.String(required=True),
        resolver=gql_ProgramUserModel.resolve_ProgramUserModel_by_roletype_id
    )
    #{'SQLTableName': 'roles', 'locals': {'id': {'name': 'id', 'type': 'graphene.String', 'column': 'id', 'isPrimaryKey': True}, 'name': {'name': 'name', 'type': 'graphene.String', 'column': 'name', 'isPrimaryKey': False}, 'lastchange': {'name': 'lastchange', 'type': 'graphene.DateTime', 'column': 'lastchange', 'isPrimaryKey': False}, 'roletype_id': {'name': 'roletype_id', 'type': 'graphene.String', 'column': 'roletype_id', 'isPrimaryKey': False}, 'user_id': {'name': 'user_id', 'type': 'graphene.String', 'column': 'user_id', 'isPrimaryKey': False}, 'group_id': {'name': 'group_id', 'type': 'graphene.String', 'column': 'group_id', 'isPrimaryKey': False}}, 'relations': {'usermodel': {'name': 'usermodel', 'useList': False, 'type': 'UserModel'}, 'roletypemodel': {'name': 'roletypemodel', 'useList': False, 'type': 'RoleTypeModel'}, 'groupmodel': {'name': 'groupmodel', 'useList': False, 'type': 'GroupModel'}}}
    #{'name': 'id', 'type': 'graphene.String', 'column': 'id', 'isPrimaryKey': True}
    roles_by_id =  graphene.Field(
        'gql_RoleModel.get_RoleModel', 
        id=graphene.String(required=True),
        resolver=gql_RoleModel.resolve_RoleModel_by_id
    )
    #{'name': 'name', 'type': 'graphene.String', 'column': 'name', 'isPrimaryKey': False}
    roles_name_starts_with =  graphene.Field(
        'gql_RoleModel.get_RoleModel', 
        name=graphene.String(required=True),
        resolver=gql_RoleModel.resolve_RoleModel_by_name
    )
    #{'name': 'lastchange', 'type': 'graphene.DateTime', 'column': 'lastchange', 'isPrimaryKey': False}
    roles_lastchange_starts_with =  graphene.Field(
        'gql_RoleModel.get_RoleModel', 
        lastchange=graphene.String(required=True),
        resolver=gql_RoleModel.resolve_RoleModel_by_lastchange
    )
    #{'name': 'roletype_id', 'type': 'graphene.String', 'column': 'roletype_id', 'isPrimaryKey': False}
    roles_roletype_id_starts_with =  graphene.Field(
        'gql_RoleModel.get_RoleModel', 
        roletype_id=graphene.String(required=True),
        resolver=gql_RoleModel.resolve_RoleModel_by_roletype_id
    )
    #{'name': 'user_id', 'type': 'graphene.String', 'column': 'user_id', 'isPrimaryKey': False}
    roles_user_id_starts_with =  graphene.Field(
        'gql_RoleModel.get_RoleModel', 
        user_id=graphene.String(required=True),
        resolver=gql_RoleModel.resolve_RoleModel_by_user_id
    )
    #{'name': 'group_id', 'type': 'graphene.String', 'column': 'group_id', 'isPrimaryKey': False}
    roles_group_id_starts_with =  graphene.Field(
        'gql_RoleModel.get_RoleModel', 
        group_id=graphene.String(required=True),
        resolver=gql_RoleModel.resolve_RoleModel_by_group_id
    )
    #{'SQLTableName': 'grouproletypes', 'locals': {'id': {'name': 'id', 'type': 'graphene.String', 'column': 'id', 'isPrimaryKey': True}, 'name': {'name': 'name', 'type': 'graphene.String', 'column': 'name', 'isPrimaryKey': False}}, 'relations': {'rolemodel_collection': {'name': 'rolemodel_collection', 'useList': True, 'type': 'RoleModel'}}}
    #{'name': 'id', 'type': 'graphene.String', 'column': 'id', 'isPrimaryKey': True}
    grouproletypes_by_id =  graphene.Field(
        'gql_RoleTypeModel.get_RoleTypeModel', 
        id=graphene.String(required=True),
        resolver=gql_RoleTypeModel.resolve_RoleTypeModel_by_id
    )
    #{'name': 'name', 'type': 'graphene.String', 'column': 'name', 'isPrimaryKey': False}
    grouproletypes_name_starts_with =  graphene.Field(
        'gql_RoleTypeModel.get_RoleTypeModel', 
        name=graphene.String(required=True),
        resolver=gql_RoleTypeModel.resolve_RoleTypeModel_by_name
    )
    #{'SQLTableName': 'rooms', 'locals': {'id': {'name': 'id', 'type': 'graphene.String', 'column': 'id', 'isPrimaryKey': True}, 'name': {'name': 'name', 'type': 'graphene.String', 'column': 'name', 'isPrimaryKey': False}, 'lastchange': {'name': 'lastchange', 'type': 'graphene.DateTime', 'column': 'lastchange', 'isPrimaryKey': False}, 'externalId': {'name': 'externalId', 'type': 'graphene.String', 'column': 'externalId', 'isPrimaryKey': False}, 'building_id': {'name': 'building_id', 'type': 'graphene.String', 'column': 'building_id', 'isPrimaryKey': False}}, 'relations': {'buildingmodel': {'name': 'buildingmodel', 'useList': False, 'type': 'BuildingModel'}, 'eventroommodel_collection': {'name': 'eventroommodel_collection', 'useList': True, 'type': 'EventRoomModel'}}}
    #{'name': 'id', 'type': 'graphene.String', 'column': 'id', 'isPrimaryKey': True}
    rooms_by_id =  graphene.Field(
        'gql_RoomModel.get_RoomModel', 
        id=graphene.String(required=True),
        resolver=gql_RoomModel.resolve_RoomModel_by_id
    )
    #{'name': 'name', 'type': 'graphene.String', 'column': 'name', 'isPrimaryKey': False}
    rooms_name_starts_with =  graphene.Field(
        'gql_RoomModel.get_RoomModel', 
        name=graphene.String(required=True),
        resolver=gql_RoomModel.resolve_RoomModel_by_name
    )
    #{'name': 'lastchange', 'type': 'graphene.DateTime', 'column': 'lastchange', 'isPrimaryKey': False}
    rooms_lastchange_starts_with =  graphene.Field(
        'gql_RoomModel.get_RoomModel', 
        lastchange=graphene.String(required=True),
        resolver=gql_RoomModel.resolve_RoomModel_by_lastchange
    )
    #{'name': 'externalId', 'type': 'graphene.String', 'column': 'externalId', 'isPrimaryKey': False}
    rooms_externalId_starts_with =  graphene.Field(
        'gql_RoomModel.get_RoomModel', 
        externalId=graphene.String(required=True),
        resolver=gql_RoomModel.resolve_RoomModel_by_externalId
    )
    #{'name': 'building_id', 'type': 'graphene.String', 'column': 'building_id', 'isPrimaryKey': False}
    rooms_building_id_starts_with =  graphene.Field(
        'gql_RoomModel.get_RoomModel', 
        building_id=graphene.String(required=True),
        resolver=gql_RoomModel.resolve_RoomModel_by_building_id
    )
    #{'SQLTableName': 'studyplans_groups', 'locals': {'id': {'name': 'id', 'type': 'graphene.String', 'column': 'id', 'isPrimaryKey': True}, 'studyplan_id': {'name': 'studyplan_id', 'type': 'graphene.String', 'column': 'studyplan_id', 'isPrimaryKey': False}, 'group_id': {'name': 'group_id', 'type': 'graphene.String', 'column': 'group_id', 'isPrimaryKey': False}}, 'relations': {'groupmodel': {'name': 'groupmodel', 'useList': False, 'type': 'GroupModel'}, 'studyplanmodel': {'name': 'studyplanmodel', 'useList': False, 'type': 'StudyPlanModel'}}}
    #{'name': 'id', 'type': 'graphene.String', 'column': 'id', 'isPrimaryKey': True}
    studyplans_groups_by_id =  graphene.Field(
        'gql_StudyPlanGroupsModel.get_StudyPlanGroupsModel', 
        id=graphene.String(required=True),
        resolver=gql_StudyPlanGroupsModel.resolve_StudyPlanGroupsModel_by_id
    )
    #{'name': 'studyplan_id', 'type': 'graphene.String', 'column': 'studyplan_id', 'isPrimaryKey': False}
    studyplans_groups_studyplan_id_starts_with =  graphene.Field(
        'gql_StudyPlanGroupsModel.get_StudyPlanGroupsModel', 
        studyplan_id=graphene.String(required=True),
        resolver=gql_StudyPlanGroupsModel.resolve_StudyPlanGroupsModel_by_studyplan_id
    )
    #{'name': 'group_id', 'type': 'graphene.String', 'column': 'group_id', 'isPrimaryKey': False}
    studyplans_groups_group_id_starts_with =  graphene.Field(
        'gql_StudyPlanGroupsModel.get_StudyPlanGroupsModel', 
        group_id=graphene.String(required=True),
        resolver=gql_StudyPlanGroupsModel.resolve_StudyPlanGroupsModel_by_group_id
    )
    #{'SQLTableName': 'studyplanitem_events', 'locals': {'id': {'name': 'id', 'type': 'graphene.String', 'column': 'id', 'isPrimaryKey': True}, 'studyplanitem_id': {'name': 'studyplanitem_id', 'type': 'graphene.String', 'column': 'studyplanitem_id', 'isPrimaryKey': False}, 'event_id': {'name': 'event_id', 'type': 'graphene.String', 'column': 'event_id', 'isPrimaryKey': False}}, 'relations': {'eventmodel': {'name': 'eventmodel', 'useList': False, 'type': 'EventModel'}, 'studyplanitemmodel': {'name': 'studyplanitemmodel', 'useList': False, 'type': 'StudyPlanItemModel'}}}
    #{'name': 'id', 'type': 'graphene.String', 'column': 'id', 'isPrimaryKey': True}
    studyplanitem_events_by_id =  graphene.Field(
        'gql_StudyPlanItemEventModel.get_StudyPlanItemEventModel', 
        id=graphene.String(required=True),
        resolver=gql_StudyPlanItemEventModel.resolve_StudyPlanItemEventModel_by_id
    )
    #{'name': 'studyplanitem_id', 'type': 'graphene.String', 'column': 'studyplanitem_id', 'isPrimaryKey': False}
    studyplanitem_events_studyplanitem_id_starts_with =  graphene.Field(
        'gql_StudyPlanItemEventModel.get_StudyPlanItemEventModel', 
        studyplanitem_id=graphene.String(required=True),
        resolver=gql_StudyPlanItemEventModel.resolve_StudyPlanItemEventModel_by_studyplanitem_id
    )
    #{'name': 'event_id', 'type': 'graphene.String', 'column': 'event_id', 'isPrimaryKey': False}
    studyplanitem_events_event_id_starts_with =  graphene.Field(
        'gql_StudyPlanItemEventModel.get_StudyPlanItemEventModel', 
        event_id=graphene.String(required=True),
        resolver=gql_StudyPlanItemEventModel.resolve_StudyPlanItemEventModel_by_event_id
    )
    #{'SQLTableName': 'studyplanitem_groups', 'locals': {'id': {'name': 'id', 'type': 'graphene.String', 'column': 'id', 'isPrimaryKey': True}, 'group_id': {'name': 'group_id', 'type': 'graphene.String', 'column': 'group_id', 'isPrimaryKey': False}, 'studyplanitem_id': {'name': 'studyplanitem_id', 'type': 'graphene.String', 'column': 'studyplanitem_id', 'isPrimaryKey': False}}, 'relations': {'studyplanitemmodel': {'name': 'studyplanitemmodel', 'useList': False, 'type': 'StudyPlanItemModel'}, 'groupmodel': {'name': 'groupmodel', 'useList': False, 'type': 'GroupModel'}}}
    #{'name': 'id', 'type': 'graphene.String', 'column': 'id', 'isPrimaryKey': True}
    studyplanitem_groups_by_id =  graphene.Field(
        'gql_StudyPlanItemGroupModel.get_StudyPlanItemGroupModel', 
        id=graphene.String(required=True),
        resolver=gql_StudyPlanItemGroupModel.resolve_StudyPlanItemGroupModel_by_id
    )
    #{'name': 'group_id', 'type': 'graphene.String', 'column': 'group_id', 'isPrimaryKey': False}
    studyplanitem_groups_group_id_starts_with =  graphene.Field(
        'gql_StudyPlanItemGroupModel.get_StudyPlanItemGroupModel', 
        group_id=graphene.String(required=True),
        resolver=gql_StudyPlanItemGroupModel.resolve_StudyPlanItemGroupModel_by_group_id
    )
    #{'name': 'studyplanitem_id', 'type': 'graphene.String', 'column': 'studyplanitem_id', 'isPrimaryKey': False}
    studyplanitem_groups_studyplanitem_id_starts_with =  graphene.Field(
        'gql_StudyPlanItemGroupModel.get_StudyPlanItemGroupModel', 
        studyplanitem_id=graphene.String(required=True),
        resolver=gql_StudyPlanItemGroupModel.resolve_StudyPlanItemGroupModel_by_studyplanitem_id
    )
    #{'SQLTableName': 'studyplanitems', 'locals': {'id': {'name': 'id', 'type': 'graphene.String', 'column': 'id', 'isPrimaryKey': True}, 'name': {'name': 'name', 'type': 'graphene.String', 'column': 'name', 'isPrimaryKey': False}, 'priority': {'name': 'priority', 'type': 'graphene.Int', 'column': 'priority', 'isPrimaryKey': False}, 'subjectSemesterTopic': {'name': 'subjectSemesterTopic', 'type': 'graphene.String', 'column': 'subjectSemesterTopic', 'isPrimaryKey': False}, 'externalId': {'name': 'externalId', 'type': 'graphene.String', 'column': 'externalId', 'isPrimaryKey': False}, 'studyplan_id': {'name': 'studyplan_id', 'type': 'graphene.String', 'column': 'studyplan_id', 'isPrimaryKey': False}}, 'relations': {'studyplanmodel': {'name': 'studyplanmodel', 'useList': False, 'type': 'StudyPlanModel'}, 'studyplanitemeventmodel_collection': {'name': 'studyplanitemeventmodel_collection', 'useList': True, 'type': 'StudyPlanItemEventModel'}, 'studyplanitemteachermodel_collection': {'name': 'studyplanitemteachermodel_collection', 'useList': True, 'type': 'StudyPlanItemTeacherModel'}, 'studyplanitemgroupmodel_collection': {'name': 'studyplanitemgroupmodel_collection', 'useList': True, 'type': 'StudyPlanItemGroupModel'}}}
    #{'name': 'id', 'type': 'graphene.String', 'column': 'id', 'isPrimaryKey': True}
    studyplanitems_by_id =  graphene.Field(
        'gql_StudyPlanItemModel.get_StudyPlanItemModel', 
        id=graphene.String(required=True),
        resolver=gql_StudyPlanItemModel.resolve_StudyPlanItemModel_by_id
    )
    #{'name': 'name', 'type': 'graphene.String', 'column': 'name', 'isPrimaryKey': False}
    studyplanitems_name_starts_with =  graphene.Field(
        'gql_StudyPlanItemModel.get_StudyPlanItemModel', 
        name=graphene.String(required=True),
        resolver=gql_StudyPlanItemModel.resolve_StudyPlanItemModel_by_name
    )
    #{'name': 'priority', 'type': 'graphene.Int', 'column': 'priority', 'isPrimaryKey': False}
    studyplanitems_priority_starts_with =  graphene.Field(
        'gql_StudyPlanItemModel.get_StudyPlanItemModel', 
        priority=graphene.String(required=True),
        resolver=gql_StudyPlanItemModel.resolve_StudyPlanItemModel_by_priority
    )
    #{'name': 'subjectSemesterTopic', 'type': 'graphene.String', 'column': 'subjectSemesterTopic', 'isPrimaryKey': False}
    studyplanitems_subjectSemesterTopic_starts_with =  graphene.Field(
        'gql_StudyPlanItemModel.get_StudyPlanItemModel', 
        subjectSemesterTopic=graphene.String(required=True),
        resolver=gql_StudyPlanItemModel.resolve_StudyPlanItemModel_by_subjectSemesterTopic
    )
    #{'name': 'externalId', 'type': 'graphene.String', 'column': 'externalId', 'isPrimaryKey': False}
    studyplanitems_externalId_starts_with =  graphene.Field(
        'gql_StudyPlanItemModel.get_StudyPlanItemModel', 
        externalId=graphene.String(required=True),
        resolver=gql_StudyPlanItemModel.resolve_StudyPlanItemModel_by_externalId
    )
    #{'name': 'studyplan_id', 'type': 'graphene.String', 'column': 'studyplan_id', 'isPrimaryKey': False}
    studyplanitems_studyplan_id_starts_with =  graphene.Field(
        'gql_StudyPlanItemModel.get_StudyPlanItemModel', 
        studyplan_id=graphene.String(required=True),
        resolver=gql_StudyPlanItemModel.resolve_StudyPlanItemModel_by_studyplan_id
    )
    #{'SQLTableName': 'studyplanitem_teachers', 'locals': {'id': {'name': 'id', 'type': 'graphene.String', 'column': 'id', 'isPrimaryKey': True}, 'teacher_id': {'name': 'teacher_id', 'type': 'graphene.String', 'column': 'teacher_id', 'isPrimaryKey': False}, 'studyplanitem_id': {'name': 'studyplanitem_id', 'type': 'graphene.String', 'column': 'studyplanitem_id', 'isPrimaryKey': False}}, 'relations': {'studyplanitemmodel': {'name': 'studyplanitemmodel', 'useList': False, 'type': 'StudyPlanItemModel'}, 'usermodel': {'name': 'usermodel', 'useList': False, 'type': 'UserModel'}}}
    #{'name': 'id', 'type': 'graphene.String', 'column': 'id', 'isPrimaryKey': True}
    studyplanitem_teachers_by_id =  graphene.Field(
        'gql_StudyPlanItemTeacherModel.get_StudyPlanItemTeacherModel', 
        id=graphene.String(required=True),
        resolver=gql_StudyPlanItemTeacherModel.resolve_StudyPlanItemTeacherModel_by_id
    )
    #{'name': 'teacher_id', 'type': 'graphene.String', 'column': 'teacher_id', 'isPrimaryKey': False}
    studyplanitem_teachers_teacher_id_starts_with =  graphene.Field(
        'gql_StudyPlanItemTeacherModel.get_StudyPlanItemTeacherModel', 
        teacher_id=graphene.String(required=True),
        resolver=gql_StudyPlanItemTeacherModel.resolve_StudyPlanItemTeacherModel_by_teacher_id
    )
    #{'name': 'studyplanitem_id', 'type': 'graphene.String', 'column': 'studyplanitem_id', 'isPrimaryKey': False}
    studyplanitem_teachers_studyplanitem_id_starts_with =  graphene.Field(
        'gql_StudyPlanItemTeacherModel.get_StudyPlanItemTeacherModel', 
        studyplanitem_id=graphene.String(required=True),
        resolver=gql_StudyPlanItemTeacherModel.resolve_StudyPlanItemTeacherModel_by_studyplanitem_id
    )
    #{'SQLTableName': 'studyplans', 'locals': {'id': {'name': 'id', 'type': 'graphene.String', 'column': 'id', 'isPrimaryKey': True}, 'name': {'name': 'name', 'type': 'graphene.String', 'column': 'name', 'isPrimaryKey': False}, 'externalId': {'name': 'externalId', 'type': 'graphene.String', 'column': 'externalId', 'isPrimaryKey': False}}, 'relations': {'studyplanitemmodel_collection': {'name': 'studyplanitemmodel_collection', 'useList': True, 'type': 'StudyPlanItemModel'}, 'studyplangroupsmodel_collection': {'name': 'studyplangroupsmodel_collection', 'useList': True, 'type': 'StudyPlanGroupsModel'}}}
    #{'name': 'id', 'type': 'graphene.String', 'column': 'id', 'isPrimaryKey': True}
    studyplans_by_id =  graphene.Field(
        'gql_StudyPlanModel.get_StudyPlanModel', 
        id=graphene.String(required=True),
        resolver=gql_StudyPlanModel.resolve_StudyPlanModel_by_id
    )
    #{'name': 'name', 'type': 'graphene.String', 'column': 'name', 'isPrimaryKey': False}
    studyplans_name_starts_with =  graphene.Field(
        'gql_StudyPlanModel.get_StudyPlanModel', 
        name=graphene.String(required=True),
        resolver=gql_StudyPlanModel.resolve_StudyPlanModel_by_name
    )
    #{'name': 'externalId', 'type': 'graphene.String', 'column': 'externalId', 'isPrimaryKey': False}
    studyplans_externalId_starts_with =  graphene.Field(
        'gql_StudyPlanModel.get_StudyPlanModel', 
        externalId=graphene.String(required=True),
        resolver=gql_StudyPlanModel.resolve_StudyPlanModel_by_externalId
    )
    #{'SQLTableName': 'subjects', 'locals': {'id': {'name': 'id', 'type': 'graphene.String', 'column': 'id', 'isPrimaryKey': True}, 'name': {'name': 'name', 'type': 'graphene.String', 'column': 'name', 'isPrimaryKey': False}, 'lastchange': {'name': 'lastchange', 'type': 'graphene.DateTime', 'column': 'lastchange', 'isPrimaryKey': False}, 'externalId': {'name': 'externalId', 'type': 'graphene.String', 'column': 'externalId', 'isPrimaryKey': False}, 'program_id': {'name': 'program_id', 'type': 'graphene.String', 'column': 'program_id', 'isPrimaryKey': False}}, 'relations': {'programmodel': {'name': 'programmodel', 'useList': False, 'type': 'ProgramModel'}, 'subjectusermodel_collection': {'name': 'subjectusermodel_collection', 'useList': True, 'type': 'SubjectUserModel'}, 'subjectsemestermodel_collection': {'name': 'subjectsemestermodel_collection', 'useList': True, 'type': 'SubjectSemesterModel'}}}
    #{'name': 'id', 'type': 'graphene.String', 'column': 'id', 'isPrimaryKey': True}
    subjects_by_id =  graphene.Field(
        'gql_SubjectModel.get_SubjectModel', 
        id=graphene.String(required=True),
        resolver=gql_SubjectModel.resolve_SubjectModel_by_id
    )
    #{'name': 'name', 'type': 'graphene.String', 'column': 'name', 'isPrimaryKey': False}
    subjects_name_starts_with =  graphene.Field(
        'gql_SubjectModel.get_SubjectModel', 
        name=graphene.String(required=True),
        resolver=gql_SubjectModel.resolve_SubjectModel_by_name
    )
    #{'name': 'lastchange', 'type': 'graphene.DateTime', 'column': 'lastchange', 'isPrimaryKey': False}
    subjects_lastchange_starts_with =  graphene.Field(
        'gql_SubjectModel.get_SubjectModel', 
        lastchange=graphene.String(required=True),
        resolver=gql_SubjectModel.resolve_SubjectModel_by_lastchange
    )
    #{'name': 'externalId', 'type': 'graphene.String', 'column': 'externalId', 'isPrimaryKey': False}
    subjects_externalId_starts_with =  graphene.Field(
        'gql_SubjectModel.get_SubjectModel', 
        externalId=graphene.String(required=True),
        resolver=gql_SubjectModel.resolve_SubjectModel_by_externalId
    )
    #{'name': 'program_id', 'type': 'graphene.String', 'column': 'program_id', 'isPrimaryKey': False}
    subjects_program_id_starts_with =  graphene.Field(
        'gql_SubjectModel.get_SubjectModel', 
        program_id=graphene.String(required=True),
        resolver=gql_SubjectModel.resolve_SubjectModel_by_program_id
    )
    #{'SQLTableName': 'subjectsemesters', 'locals': {'id': {'name': 'id', 'type': 'graphene.String', 'column': 'id', 'isPrimaryKey': True}, 'name': {'name': 'name', 'type': 'graphene.String', 'column': 'name', 'isPrimaryKey': False}, 'lastchange': {'name': 'lastchange', 'type': 'graphene.DateTime', 'column': 'lastchange', 'isPrimaryKey': False}, 'subject_id': {'name': 'subject_id', 'type': 'graphene.String', 'column': 'subject_id', 'isPrimaryKey': False}}, 'relations': {'subjectmodel': {'name': 'subjectmodel', 'useList': False, 'type': 'SubjectModel'}, 'subjecttopicmodel_collection': {'name': 'subjecttopicmodel_collection', 'useList': True, 'type': 'SubjectTopicModel'}}}
    #{'name': 'id', 'type': 'graphene.String', 'column': 'id', 'isPrimaryKey': True}
    subjectsemesters_by_id =  graphene.Field(
        'gql_SubjectSemesterModel.get_SubjectSemesterModel', 
        id=graphene.String(required=True),
        resolver=gql_SubjectSemesterModel.resolve_SubjectSemesterModel_by_id
    )
    #{'name': 'name', 'type': 'graphene.String', 'column': 'name', 'isPrimaryKey': False}
    subjectsemesters_name_starts_with =  graphene.Field(
        'gql_SubjectSemesterModel.get_SubjectSemesterModel', 
        name=graphene.String(required=True),
        resolver=gql_SubjectSemesterModel.resolve_SubjectSemesterModel_by_name
    )
    #{'name': 'lastchange', 'type': 'graphene.DateTime', 'column': 'lastchange', 'isPrimaryKey': False}
    subjectsemesters_lastchange_starts_with =  graphene.Field(
        'gql_SubjectSemesterModel.get_SubjectSemesterModel', 
        lastchange=graphene.String(required=True),
        resolver=gql_SubjectSemesterModel.resolve_SubjectSemesterModel_by_lastchange
    )
    #{'name': 'subject_id', 'type': 'graphene.String', 'column': 'subject_id', 'isPrimaryKey': False}
    subjectsemesters_subject_id_starts_with =  graphene.Field(
        'gql_SubjectSemesterModel.get_SubjectSemesterModel', 
        subject_id=graphene.String(required=True),
        resolver=gql_SubjectSemesterModel.resolve_SubjectSemesterModel_by_subject_id
    )
    #{'SQLTableName': 'subjecttopics', 'locals': {'id': {'name': 'id', 'type': 'graphene.String', 'column': 'id', 'isPrimaryKey': True}, 'name': {'name': 'name', 'type': 'graphene.String', 'column': 'name', 'isPrimaryKey': False}, 'externalId': {'name': 'externalId', 'type': 'graphene.String', 'column': 'externalId', 'isPrimaryKey': False}, 'subjectsemester_id': {'name': 'subjectsemester_id', 'type': 'graphene.String', 'column': 'subjectsemester_id', 'isPrimaryKey': False}}, 'relations': {'subjectsemestermodel': {'name': 'subjectsemestermodel', 'useList': False, 'type': 'SubjectSemesterModel'}, 'subjecttopicusermodel_collection': {'name': 'subjecttopicusermodel_collection', 'useList': True, 'type': 'SubjectTopicUserModel'}}}
    #{'name': 'id', 'type': 'graphene.String', 'column': 'id', 'isPrimaryKey': True}
    subjecttopics_by_id =  graphene.Field(
        'gql_SubjectTopicModel.get_SubjectTopicModel', 
        id=graphene.String(required=True),
        resolver=gql_SubjectTopicModel.resolve_SubjectTopicModel_by_id
    )
    #{'name': 'name', 'type': 'graphene.String', 'column': 'name', 'isPrimaryKey': False}
    subjecttopics_name_starts_with =  graphene.Field(
        'gql_SubjectTopicModel.get_SubjectTopicModel', 
        name=graphene.String(required=True),
        resolver=gql_SubjectTopicModel.resolve_SubjectTopicModel_by_name
    )
    #{'name': 'externalId', 'type': 'graphene.String', 'column': 'externalId', 'isPrimaryKey': False}
    subjecttopics_externalId_starts_with =  graphene.Field(
        'gql_SubjectTopicModel.get_SubjectTopicModel', 
        externalId=graphene.String(required=True),
        resolver=gql_SubjectTopicModel.resolve_SubjectTopicModel_by_externalId
    )
    #{'name': 'subjectsemester_id', 'type': 'graphene.String', 'column': 'subjectsemester_id', 'isPrimaryKey': False}
    subjecttopics_subjectsemester_id_starts_with =  graphene.Field(
        'gql_SubjectTopicModel.get_SubjectTopicModel', 
        subjectsemester_id=graphene.String(required=True),
        resolver=gql_SubjectTopicModel.resolve_SubjectTopicModel_by_subjectsemester_id
    )
    #{'SQLTableName': 'subjecttopics_users', 'locals': {'id': {'name': 'id', 'type': 'graphene.String', 'column': 'id', 'isPrimaryKey': True}, 'subjecttopic_id': {'name': 'subjecttopic_id', 'type': 'graphene.String', 'column': 'subjecttopic_id', 'isPrimaryKey': False}, 'user_id': {'name': 'user_id', 'type': 'graphene.String', 'column': 'user_id', 'isPrimaryKey': False}, 'roletype_id': {'name': 'roletype_id', 'type': 'graphene.String', 'column': 'roletype_id', 'isPrimaryKey': False}}, 'relations': {'subjecttopicmodel': {'name': 'subjecttopicmodel', 'useList': False, 'type': 'SubjectTopicModel'}, 'usermodel': {'name': 'usermodel', 'useList': False, 'type': 'UserModel'}, 'acreditationuserroletypemodel': {'name': 'acreditationuserroletypemodel', 'useList': False, 'type': 'AcreditationUserRoleTypeModel'}}}
    #{'name': 'id', 'type': 'graphene.String', 'column': 'id', 'isPrimaryKey': True}
    subjecttopics_users_by_id =  graphene.Field(
        'gql_SubjectTopicUserModel.get_SubjectTopicUserModel', 
        id=graphene.String(required=True),
        resolver=gql_SubjectTopicUserModel.resolve_SubjectTopicUserModel_by_id
    )
    #{'name': 'subjecttopic_id', 'type': 'graphene.String', 'column': 'subjecttopic_id', 'isPrimaryKey': False}
    subjecttopics_users_subjecttopic_id_starts_with =  graphene.Field(
        'gql_SubjectTopicUserModel.get_SubjectTopicUserModel', 
        subjecttopic_id=graphene.String(required=True),
        resolver=gql_SubjectTopicUserModel.resolve_SubjectTopicUserModel_by_subjecttopic_id
    )
    #{'name': 'user_id', 'type': 'graphene.String', 'column': 'user_id', 'isPrimaryKey': False}
    subjecttopics_users_user_id_starts_with =  graphene.Field(
        'gql_SubjectTopicUserModel.get_SubjectTopicUserModel', 
        user_id=graphene.String(required=True),
        resolver=gql_SubjectTopicUserModel.resolve_SubjectTopicUserModel_by_user_id
    )
    #{'name': 'roletype_id', 'type': 'graphene.String', 'column': 'roletype_id', 'isPrimaryKey': False}
    subjecttopics_users_roletype_id_starts_with =  graphene.Field(
        'gql_SubjectTopicUserModel.get_SubjectTopicUserModel', 
        roletype_id=graphene.String(required=True),
        resolver=gql_SubjectTopicUserModel.resolve_SubjectTopicUserModel_by_roletype_id
    )
    #{'SQLTableName': 'subjects_users', 'locals': {'id': {'name': 'id', 'type': 'graphene.String', 'column': 'id', 'isPrimaryKey': True}, 'subject_id': {'name': 'subject_id', 'type': 'graphene.String', 'column': 'subject_id', 'isPrimaryKey': False}, 'user_id': {'name': 'user_id', 'type': 'graphene.String', 'column': 'user_id', 'isPrimaryKey': False}, 'roletype_id': {'name': 'roletype_id', 'type': 'graphene.String', 'column': 'roletype_id', 'isPrimaryKey': False}}, 'relations': {'usermodel': {'name': 'usermodel', 'useList': False, 'type': 'UserModel'}, 'subjectmodel': {'name': 'subjectmodel', 'useList': False, 'type': 'SubjectModel'}, 'acreditationuserroletypemodel': {'name': 'acreditationuserroletypemodel', 'useList': False, 'type': 'AcreditationUserRoleTypeModel'}}}
    #{'name': 'id', 'type': 'graphene.String', 'column': 'id', 'isPrimaryKey': True}
    subjects_users_by_id =  graphene.Field(
        'gql_SubjectUserModel.get_SubjectUserModel', 
        id=graphene.String(required=True),
        resolver=gql_SubjectUserModel.resolve_SubjectUserModel_by_id
    )
    #{'name': 'subject_id', 'type': 'graphene.String', 'column': 'subject_id', 'isPrimaryKey': False}
    subjects_users_subject_id_starts_with =  graphene.Field(
        'gql_SubjectUserModel.get_SubjectUserModel', 
        subject_id=graphene.String(required=True),
        resolver=gql_SubjectUserModel.resolve_SubjectUserModel_by_subject_id
    )
    #{'name': 'user_id', 'type': 'graphene.String', 'column': 'user_id', 'isPrimaryKey': False}
    subjects_users_user_id_starts_with =  graphene.Field(
        'gql_SubjectUserModel.get_SubjectUserModel', 
        user_id=graphene.String(required=True),
        resolver=gql_SubjectUserModel.resolve_SubjectUserModel_by_user_id
    )
    #{'name': 'roletype_id', 'type': 'graphene.String', 'column': 'roletype_id', 'isPrimaryKey': False}
    subjects_users_roletype_id_starts_with =  graphene.Field(
        'gql_SubjectUserModel.get_SubjectUserModel', 
        roletype_id=graphene.String(required=True),
        resolver=gql_SubjectUserModel.resolve_SubjectUserModel_by_roletype_id
    )
    #{'SQLTableName': 'users_groups', 'locals': {'id': {'name': 'id', 'type': 'graphene.String', 'column': 'id', 'isPrimaryKey': True}, 'user_id': {'name': 'user_id', 'type': 'graphene.String', 'column': 'user_id', 'isPrimaryKey': False}, 'group_id': {'name': 'group_id', 'type': 'graphene.String', 'column': 'group_id', 'isPrimaryKey': False}}, 'relations': {'usermodel': {'name': 'usermodel', 'useList': False, 'type': 'UserModel'}, 'groupmodel': {'name': 'groupmodel', 'useList': False, 'type': 'GroupModel'}}}
    #{'name': 'id', 'type': 'graphene.String', 'column': 'id', 'isPrimaryKey': True}
    users_groups_by_id =  graphene.Field(
        'gql_UserGroupModel.get_UserGroupModel', 
        id=graphene.String(required=True),
        resolver=gql_UserGroupModel.resolve_UserGroupModel_by_id
    )
    #{'name': 'user_id', 'type': 'graphene.String', 'column': 'user_id', 'isPrimaryKey': False}
    users_groups_user_id_starts_with =  graphene.Field(
        'gql_UserGroupModel.get_UserGroupModel', 
        user_id=graphene.String(required=True),
        resolver=gql_UserGroupModel.resolve_UserGroupModel_by_user_id
    )
    #{'name': 'group_id', 'type': 'graphene.String', 'column': 'group_id', 'isPrimaryKey': False}
    users_groups_group_id_starts_with =  graphene.Field(
        'gql_UserGroupModel.get_UserGroupModel', 
        group_id=graphene.String(required=True),
        resolver=gql_UserGroupModel.resolve_UserGroupModel_by_group_id
    )
    #{'SQLTableName': 'users', 'locals': {'id': {'name': 'id', 'type': 'graphene.String', 'column': 'id', 'isPrimaryKey': True}, 'name': {'name': 'name', 'type': 'graphene.String', 'column': 'name', 'isPrimaryKey': False}, 'surname': {'name': 'surname', 'type': 'graphene.String', 'column': 'surname', 'isPrimaryKey': False}, 'email': {'name': 'email', 'type': 'graphene.String', 'column': 'email', 'isPrimaryKey': False}, 'lastchange': {'name': 'lastchange', 'type': 'graphene.DateTime', 'column': 'lastchange', 'isPrimaryKey': False}, 'externalId': {'name': 'externalId', 'type': 'graphene.Int', 'column': 'externalId', 'isPrimaryKey': False}, 'UCO': {'name': 'UCO', 'type': 'graphene.String', 'column': 'UCO', 'isPrimaryKey': False}, 'VaVId': {'name': 'VaVId', 'type': 'graphene.String', 'column': 'VaVId', 'isPrimaryKey': False}}, 'relations': {'eventusermodel_collection': {'name': 'eventusermodel_collection', 'useList': True, 'type': 'EventUserModel'}, 'programusermodel_collection': {'name': 'programusermodel_collection', 'useList': True, 'type': 'ProgramUserModel'}, 'usergroupmodel_collection': {'name': 'usergroupmodel_collection', 'useList': True, 'type': 'UserGroupModel'}, 'rolemodel_collection': {'name': 'rolemodel_collection', 'useList': True, 'type': 'RoleModel'}, 'subjectusermodel_collection': {'name': 'subjectusermodel_collection', 'useList': True, 'type': 'SubjectUserModel'}, 'studyplanitemteachermodel_collection': {'name': 'studyplanitemteachermodel_collection', 'useList': True, 'type': 'StudyPlanItemTeacherModel'}, 'subjecttopicusermodel_collection': {'name': 'subjecttopicusermodel_collection', 'useList': True, 'type': 'SubjectTopicUserModel'}}}
    #{'name': 'id', 'type': 'graphene.String', 'column': 'id', 'isPrimaryKey': True}
    users_by_id =  graphene.Field(
        'gql_UserModel.get_UserModel', 
        id=graphene.String(required=True),
        resolver=gql_UserModel.resolve_UserModel_by_id
    )
    #{'name': 'name', 'type': 'graphene.String', 'column': 'name', 'isPrimaryKey': False}
    users_name_starts_with =  graphene.Field(
        'gql_UserModel.get_UserModel', 
        name=graphene.String(required=True),
        resolver=gql_UserModel.resolve_UserModel_by_name
    )
    #{'name': 'surname', 'type': 'graphene.String', 'column': 'surname', 'isPrimaryKey': False}
    users_surname_starts_with =  graphene.Field(
        'gql_UserModel.get_UserModel', 
        surname=graphene.String(required=True),
        resolver=gql_UserModel.resolve_UserModel_by_surname
    )
    #{'name': 'email', 'type': 'graphene.String', 'column': 'email', 'isPrimaryKey': False}
    users_email_starts_with =  graphene.Field(
        'gql_UserModel.get_UserModel', 
        email=graphene.String(required=True),
        resolver=gql_UserModel.resolve_UserModel_by_email
    )
    #{'name': 'lastchange', 'type': 'graphene.DateTime', 'column': 'lastchange', 'isPrimaryKey': False}
    users_lastchange_starts_with =  graphene.Field(
        'gql_UserModel.get_UserModel', 
        lastchange=graphene.String(required=True),
        resolver=gql_UserModel.resolve_UserModel_by_lastchange
    )
    #{'name': 'externalId', 'type': 'graphene.Int', 'column': 'externalId', 'isPrimaryKey': False}
    users_externalId_starts_with =  graphene.Field(
        'gql_UserModel.get_UserModel', 
        externalId=graphene.String(required=True),
        resolver=gql_UserModel.resolve_UserModel_by_externalId
    )
    #{'name': 'UCO', 'type': 'graphene.String', 'column': 'UCO', 'isPrimaryKey': False}
    users_UCO_starts_with =  graphene.Field(
        'gql_UserModel.get_UserModel', 
        UCO=graphene.String(required=True),
        resolver=gql_UserModel.resolve_UserModel_by_UCO
    )
    #{'name': 'VaVId', 'type': 'graphene.String', 'column': 'VaVId', 'isPrimaryKey': False}
    users_VaVId_starts_with =  graphene.Field(
        'gql_UserModel.get_UserModel', 
        VaVId=graphene.String(required=True),
        resolver=gql_UserModel.resolve_UserModel_by_VaVId
    )

def attachGraphQL(app, sessionFunc, bindPoint='/gql'):

    """Attaches a Swagger endpoint to a FastAPI

    Parameters
    ----------
    app: FastAPI
        app to bind to
    prepareSession: lambda : session
        callable which returns a db session
    """
    assert callable(sessionFunc), "sessionFunc must be a function creating a session"

    session_scope = contextmanager(sessionFunc)

    class localSchema(graphene.Schema):
        def __init__(self, *args, **kwargs) -> None:
            super().__init__(*args, **kwargs)

        def execute(self, *args, **kwargs):
            with session_scope() as session:
                if 'context' in kwargs:
                    newkwargs = {**kwargs, 'context': {**kwargs['context'], 'session': session}}
                else:
                    newkwargs = {**kwargs, 'context': {'session': session}}
                return super().execute(*args, **newkwargs)

        async def execute_async(self, *args, **kwargs):
            with session_scope() as session:
                if 'context' in kwargs:
                    newkwargs = {**kwargs, 'context': {**kwargs['context'], 'session': session}}
                else:
                    newkwargs = {**kwargs, 'context': {'session': session}}
                return await super().execute_async(*args, **newkwargs)

    from starlette.graphql import GraphQLApp
    
    #graphql_app = GraphQLApp(schema=localSchema(query=query, mutation=createMutationRoot()))
    graphql_app = GraphQLApp(schema=localSchema(query=query))
    
    app.add_route(bindPoint, graphql_app)