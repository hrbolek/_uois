import graphene
from contextlib import contextmanager


from . import gql_AcreditationUserRoleTypeModel
from . import gql_ArealModel
from . import gql_BuildingModel
from . import gql_EventGroupModel
from . import gql_EventModel
from . import gql_EventRoomModel
from . import gql_EventUserModel
from . import gql_GroupConnectionModel
from . import gql_GroupModel
from . import gql_GroupTypeModel
from . import gql_ProgramModel
from . import gql_ProgramUserModel
from . import gql_RoleModel
from . import gql_RoleTypeModel
from . import gql_RoomModel
from . import gql_StudyPlanGroupsModel
from . import gql_StudyPlanItemEventModel
from . import gql_StudyPlanItemGroupModel
from . import gql_StudyPlanItemModel
from . import gql_StudyPlanItemTeacherModel
from . import gql_StudyPlanModel
from . import gql_SubjectModel
from . import gql_SubjectSemesterModel
from . import gql_SubjectTopicModel
from . import gql_SubjectTopicUserModel
from . import gql_SubjectUserModel
from . import gql_UserGroupModel
from . import gql_UserModel

class query(graphene.ObjectType):

    #{'SQLTableName': 'acreditationuserroletypes', 'locals': {'id': {'name': 'id', 'type': 'graphene.String', 'column': 'id', 'isPrimaryKey': True}, 'name': {'name': 'name', 'type': 'graphene.String', 'column': 'name', 'isPrimaryKey': False}}, 'relations': {'programusermodels': {'name': 'programusermodels', 'useList': True, 'type': 'ProgramUserModel'}, 'subjectusermodels': {'name': 'subjectusermodels', 'useList': True, 'type': 'SubjectUserModel'}, 'subjecttopicusermodels': {'name': 'subjecttopicusermodels', 'useList': True, 'type': 'SubjectTopicUserModel'}}}
    #{'name': 'id', 'type': 'graphene.String', 'column': 'id', 'isPrimaryKey': True}
    acreditationuserroletypes_by_id =  graphene.Field(
        'graphqltypes.gql_AcreditationUserRoleTypeModel.AcreditationUserRoleTypeModel', 
        id=graphene.String(required=True),
        resolver=gql_AcreditationUserRoleTypeModel.resolve_acreditationuserroletypes_by_id
    )
    #{'name': 'name', 'type': 'graphene.String', 'column': 'name', 'isPrimaryKey': False}
    acreditationuserroletypes_name_starts_with =  graphene.Field(
        'graphqltypes.gql_AcreditationUserRoleTypeModel.AcreditationUserRoleTypeModel', 
        name=graphene.String(required=True),
        resolver=gql_AcreditationUserRoleTypeModel.resolve_acreditationuserroletypes_name_starts_with
    )
    #{'SQLTableName': 'areals', 'locals': {'id': {'name': 'id', 'type': 'graphene.String', 'column': 'id', 'isPrimaryKey': True}, 'name': {'name': 'name', 'type': 'graphene.String', 'column': 'name', 'isPrimaryKey': False}, 'externalId': {'name': 'externalId', 'type': 'graphene.String', 'column': 'externalId', 'isPrimaryKey': False}, 'lastchange': {'name': 'lastchange', 'type': 'graphene.DateTime', 'column': 'lastchange', 'isPrimaryKey': False}}, 'relations': {'buildingmodels': {'name': 'buildingmodels', 'useList': True, 'type': 'BuildingModel'}}}
    #{'name': 'id', 'type': 'graphene.String', 'column': 'id', 'isPrimaryKey': True}
    areals_by_id =  graphene.Field(
        'graphqltypes.gql_ArealModel.ArealModel', 
        id=graphene.String(required=True),
        resolver=gql_ArealModel.resolve_areals_by_id
    )
    #{'name': 'name', 'type': 'graphene.String', 'column': 'name', 'isPrimaryKey': False}
    areals_name_starts_with =  graphene.Field(
        'graphqltypes.gql_ArealModel.ArealModel', 
        name=graphene.String(required=True),
        resolver=gql_ArealModel.resolve_areals_name_starts_with
    )
    #{'name': 'externalId', 'type': 'graphene.String', 'column': 'externalId', 'isPrimaryKey': False}
    areals_externalId_starts_with =  graphene.Field(
        'graphqltypes.gql_ArealModel.ArealModel', 
        externalId=graphene.String(required=True),
        resolver=gql_ArealModel.resolve_areals_externalId_starts_with
    )
    #{'name': 'lastchange', 'type': 'graphene.DateTime', 'column': 'lastchange', 'isPrimaryKey': False}
    areals_lastchange_starts_with =  graphene.Field(
        'graphqltypes.gql_ArealModel.ArealModel', 
        lastchange=graphene.String(required=True),
        resolver=gql_ArealModel.resolve_areals_lastchange_starts_with
    )
    #{'SQLTableName': 'buildings', 'locals': {'id': {'name': 'id', 'type': 'graphene.String', 'column': 'id', 'isPrimaryKey': True}, 'name': {'name': 'name', 'type': 'graphene.String', 'column': 'name', 'isPrimaryKey': False}, 'lastchange': {'name': 'lastchange', 'type': 'graphene.DateTime', 'column': 'lastchange', 'isPrimaryKey': False}, 'externalId': {'name': 'externalId', 'type': 'graphene.String', 'column': 'externalId', 'isPrimaryKey': False}, 'areal_id': {'name': 'areal_id', 'type': 'graphene.String', 'column': 'areal_id', 'isPrimaryKey': False}}, 'relations': {'arealmodel': {'name': 'arealmodel', 'useList': False, 'type': 'ArealModel'}, 'roommodels': {'name': 'roommodels', 'useList': True, 'type': 'RoomModel'}}}
    #{'name': 'id', 'type': 'graphene.String', 'column': 'id', 'isPrimaryKey': True}
    buildings_by_id =  graphene.Field(
        'graphqltypes.gql_BuildingModel.BuildingModel', 
        id=graphene.String(required=True),
        resolver=gql_BuildingModel.resolve_buildings_by_id
    )
    #{'name': 'name', 'type': 'graphene.String', 'column': 'name', 'isPrimaryKey': False}
    buildings_name_starts_with =  graphene.Field(
        'graphqltypes.gql_BuildingModel.BuildingModel', 
        name=graphene.String(required=True),
        resolver=gql_BuildingModel.resolve_buildings_name_starts_with
    )
    #{'name': 'lastchange', 'type': 'graphene.DateTime', 'column': 'lastchange', 'isPrimaryKey': False}
    buildings_lastchange_starts_with =  graphene.Field(
        'graphqltypes.gql_BuildingModel.BuildingModel', 
        lastchange=graphene.String(required=True),
        resolver=gql_BuildingModel.resolve_buildings_lastchange_starts_with
    )
    #{'name': 'externalId', 'type': 'graphene.String', 'column': 'externalId', 'isPrimaryKey': False}
    buildings_externalId_starts_with =  graphene.Field(
        'graphqltypes.gql_BuildingModel.BuildingModel', 
        externalId=graphene.String(required=True),
        resolver=gql_BuildingModel.resolve_buildings_externalId_starts_with
    )
    #{'name': 'areal_id', 'type': 'graphene.String', 'column': 'areal_id', 'isPrimaryKey': False}
    buildings_areal_id_starts_with =  graphene.Field(
        'graphqltypes.gql_BuildingModel.BuildingModel', 
        areal_id=graphene.String(required=True),
        resolver=gql_BuildingModel.resolve_buildings_areal_id_starts_with
    )
    #{'SQLTableName': 'events_groups', 'locals': {'id': {'name': 'id', 'type': 'graphene.String', 'column': 'id', 'isPrimaryKey': True}, 'group_id': {'name': 'group_id', 'type': 'graphene.String', 'column': 'group_id', 'isPrimaryKey': False}, 'event_id': {'name': 'event_id', 'type': 'graphene.String', 'column': 'event_id', 'isPrimaryKey': False}}, 'relations': {'eventmodel': {'name': 'eventmodel', 'useList': False, 'type': 'EventModel'}, 'groupmodel': {'name': 'groupmodel', 'useList': False, 'type': 'GroupModel'}}}
    #{'name': 'id', 'type': 'graphene.String', 'column': 'id', 'isPrimaryKey': True}
    events_groups_by_id =  graphene.Field(
        'graphqltypes.gql_EventGroupModel.EventGroupModel', 
        id=graphene.String(required=True),
        resolver=gql_EventGroupModel.resolve_events_groups_by_id
    )
    #{'name': 'group_id', 'type': 'graphene.String', 'column': 'group_id', 'isPrimaryKey': False}
    events_groups_group_id_starts_with =  graphene.Field(
        'graphqltypes.gql_EventGroupModel.EventGroupModel', 
        group_id=graphene.String(required=True),
        resolver=gql_EventGroupModel.resolve_events_groups_group_id_starts_with
    )
    #{'name': 'event_id', 'type': 'graphene.String', 'column': 'event_id', 'isPrimaryKey': False}
    events_groups_event_id_starts_with =  graphene.Field(
        'graphqltypes.gql_EventGroupModel.EventGroupModel', 
        event_id=graphene.String(required=True),
        resolver=gql_EventGroupModel.resolve_events_groups_event_id_starts_with
    )
    #{'SQLTableName': 'events', 'locals': {'id': {'name': 'id', 'type': 'graphene.String', 'column': 'id', 'isPrimaryKey': True}, 'start': {'name': 'start', 'type': 'graphene.DateTime', 'column': 'start', 'isPrimaryKey': False}, 'end': {'name': 'end', 'type': 'graphene.DateTime', 'column': 'end', 'isPrimaryKey': False}, 'label': {'name': 'label', 'type': 'graphene.String', 'column': 'label', 'isPrimaryKey': False}, 'externalId': {'name': 'externalId', 'type': 'graphene.String', 'column': 'externalId', 'isPrimaryKey': False}, 'lastchange': {'name': 'lastchange', 'type': 'graphene.DateTime', 'column': 'lastchange', 'isPrimaryKey': False}}, 'relations': {'eventusermodels': {'name': 'eventusermodels', 'useList': True, 'type': 'EventUserModel'}, 'eventgroupmodels': {'name': 'eventgroupmodels', 'useList': True, 'type': 'EventGroupModel'}, 'studyplanitemeventmodels': {'name': 'studyplanitemeventmodels', 'useList': True, 'type': 'StudyPlanItemEventModel'}, 'eventroommodels': {'name': 'eventroommodels', 'useList': True, 'type': 'EventRoomModel'}}}
    #{'name': 'id', 'type': 'graphene.String', 'column': 'id', 'isPrimaryKey': True}
    events_by_id =  graphene.Field(
        'graphqltypes.gql_EventModel.EventModel', 
        id=graphene.String(required=True),
        resolver=gql_EventModel.resolve_events_by_id
    )
    #{'name': 'start', 'type': 'graphene.DateTime', 'column': 'start', 'isPrimaryKey': False}
    events_start_starts_with =  graphene.Field(
        'graphqltypes.gql_EventModel.EventModel', 
        start=graphene.String(required=True),
        resolver=gql_EventModel.resolve_events_start_starts_with
    )
    #{'name': 'end', 'type': 'graphene.DateTime', 'column': 'end', 'isPrimaryKey': False}
    events_end_starts_with =  graphene.Field(
        'graphqltypes.gql_EventModel.EventModel', 
        end=graphene.String(required=True),
        resolver=gql_EventModel.resolve_events_end_starts_with
    )
    #{'name': 'label', 'type': 'graphene.String', 'column': 'label', 'isPrimaryKey': False}
    events_label_starts_with =  graphene.Field(
        'graphqltypes.gql_EventModel.EventModel', 
        label=graphene.String(required=True),
        resolver=gql_EventModel.resolve_events_label_starts_with
    )
    #{'name': 'externalId', 'type': 'graphene.String', 'column': 'externalId', 'isPrimaryKey': False}
    events_externalId_starts_with =  graphene.Field(
        'graphqltypes.gql_EventModel.EventModel', 
        externalId=graphene.String(required=True),
        resolver=gql_EventModel.resolve_events_externalId_starts_with
    )
    #{'name': 'lastchange', 'type': 'graphene.DateTime', 'column': 'lastchange', 'isPrimaryKey': False}
    events_lastchange_starts_with =  graphene.Field(
        'graphqltypes.gql_EventModel.EventModel', 
        lastchange=graphene.String(required=True),
        resolver=gql_EventModel.resolve_events_lastchange_starts_with
    )
    #{'SQLTableName': 'events_rooms', 'locals': {'id': {'name': 'id', 'type': 'graphene.String', 'column': 'id', 'isPrimaryKey': True}, 'room_id': {'name': 'room_id', 'type': 'graphene.String', 'column': 'room_id', 'isPrimaryKey': False}, 'event_id': {'name': 'event_id', 'type': 'graphene.String', 'column': 'event_id', 'isPrimaryKey': False}}, 'relations': {'roommodel': {'name': 'roommodel', 'useList': False, 'type': 'RoomModel'}, 'eventmodel': {'name': 'eventmodel', 'useList': False, 'type': 'EventModel'}}}
    #{'name': 'id', 'type': 'graphene.String', 'column': 'id', 'isPrimaryKey': True}
    events_rooms_by_id =  graphene.Field(
        'graphqltypes.gql_EventRoomModel.EventRoomModel', 
        id=graphene.String(required=True),
        resolver=gql_EventRoomModel.resolve_events_rooms_by_id
    )
    #{'name': 'room_id', 'type': 'graphene.String', 'column': 'room_id', 'isPrimaryKey': False}
    events_rooms_room_id_starts_with =  graphene.Field(
        'graphqltypes.gql_EventRoomModel.EventRoomModel', 
        room_id=graphene.String(required=True),
        resolver=gql_EventRoomModel.resolve_events_rooms_room_id_starts_with
    )
    #{'name': 'event_id', 'type': 'graphene.String', 'column': 'event_id', 'isPrimaryKey': False}
    events_rooms_event_id_starts_with =  graphene.Field(
        'graphqltypes.gql_EventRoomModel.EventRoomModel', 
        event_id=graphene.String(required=True),
        resolver=gql_EventRoomModel.resolve_events_rooms_event_id_starts_with
    )
    #{'SQLTableName': 'events_users', 'locals': {'id': {'name': 'id', 'type': 'graphene.String', 'column': 'id', 'isPrimaryKey': True}, 'user_id': {'name': 'user_id', 'type': 'graphene.String', 'column': 'user_id', 'isPrimaryKey': False}, 'event_id': {'name': 'event_id', 'type': 'graphene.String', 'column': 'event_id', 'isPrimaryKey': False}}, 'relations': {'usermodel': {'name': 'usermodel', 'useList': False, 'type': 'UserModel'}, 'eventmodel': {'name': 'eventmodel', 'useList': False, 'type': 'EventModel'}}}
    #{'name': 'id', 'type': 'graphene.String', 'column': 'id', 'isPrimaryKey': True}
    events_users_by_id =  graphene.Field(
        'graphqltypes.gql_EventUserModel.EventUserModel', 
        id=graphene.String(required=True),
        resolver=gql_EventUserModel.resolve_events_users_by_id
    )
    #{'name': 'user_id', 'type': 'graphene.String', 'column': 'user_id', 'isPrimaryKey': False}
    events_users_user_id_starts_with =  graphene.Field(
        'graphqltypes.gql_EventUserModel.EventUserModel', 
        user_id=graphene.String(required=True),
        resolver=gql_EventUserModel.resolve_events_users_user_id_starts_with
    )
    #{'name': 'event_id', 'type': 'graphene.String', 'column': 'event_id', 'isPrimaryKey': False}
    events_users_event_id_starts_with =  graphene.Field(
        'graphqltypes.gql_EventUserModel.EventUserModel', 
        event_id=graphene.String(required=True),
        resolver=gql_EventUserModel.resolve_events_users_event_id_starts_with
    )
    #{'SQLTableName': 'groups_groups', 'locals': {'id': {'name': 'id', 'type': 'graphene.String', 'column': 'id', 'isPrimaryKey': True}, 'child_id': {'name': 'child_id', 'type': 'graphene.String', 'column': 'child_id', 'isPrimaryKey': False}, 'parent_id': {'name': 'parent_id', 'type': 'graphene.String', 'column': 'parent_id', 'isPrimaryKey': False}}, 'relations': {'groupmodel': {'name': 'groupmodel', 'useList': False, 'type': 'GroupModel'}}}
    #{'name': 'id', 'type': 'graphene.String', 'column': 'id', 'isPrimaryKey': True}
    groups_groups_by_id =  graphene.Field(
        'graphqltypes.gql_GroupConnectionModel.GroupConnectionModel', 
        id=graphene.String(required=True),
        resolver=gql_GroupConnectionModel.resolve_groups_groups_by_id
    )
    #{'name': 'child_id', 'type': 'graphene.String', 'column': 'child_id', 'isPrimaryKey': False}
    groups_groups_child_id_starts_with =  graphene.Field(
        'graphqltypes.gql_GroupConnectionModel.GroupConnectionModel', 
        child_id=graphene.String(required=True),
        resolver=gql_GroupConnectionModel.resolve_groups_groups_child_id_starts_with
    )
    #{'name': 'parent_id', 'type': 'graphene.String', 'column': 'parent_id', 'isPrimaryKey': False}
    groups_groups_parent_id_starts_with =  graphene.Field(
        'graphqltypes.gql_GroupConnectionModel.GroupConnectionModel', 
        parent_id=graphene.String(required=True),
        resolver=gql_GroupConnectionModel.resolve_groups_groups_parent_id_starts_with
    )
    #{'SQLTableName': 'groups', 'locals': {'id': {'name': 'id', 'type': 'graphene.String', 'column': 'id', 'isPrimaryKey': True}, 'name': {'name': 'name', 'type': 'graphene.String', 'column': 'name', 'isPrimaryKey': False}, 'abbreviation': {'name': 'abbreviation', 'type': 'graphene.String', 'column': 'abbreviation', 'isPrimaryKey': False}, 'lastchange': {'name': 'lastchange', 'type': 'graphene.DateTime', 'column': 'lastchange', 'isPrimaryKey': False}, 'entryYearId': {'name': 'entryYearId', 'type': 'graphene.Int', 'column': 'entryYearId', 'isPrimaryKey': False}, 'externalId': {'name': 'externalId', 'type': 'graphene.String', 'column': 'externalId', 'isPrimaryKey': False}, 'UIC': {'name': 'UIC', 'type': 'graphene.String', 'column': 'UIC', 'isPrimaryKey': False}, 'grouptype_id': {'name': 'grouptype_id', 'type': 'graphene.String', 'column': 'grouptype_id', 'isPrimaryKey': False}}, 'relations': {'grouptypemodel': {'name': 'grouptypemodel', 'useList': False, 'type': 'GroupTypeModel'}, 'groupconnectionmodels': {'name': 'groupconnectionmodels', 'useList': True, 'type': 'GroupConnectionModel'}, 'usergroupmodels': {'name': 'usergroupmodels', 'useList': True, 'type': 'UserGroupModel'}, 'rolemodels': {'name': 'rolemodels', 'useList': True, 'type': 'RoleModel'}, 'eventgroupmodels': {'name': 'eventgroupmodels', 'useList': True, 'type': 'EventGroupModel'}, 'studyplangroupsmodels': {'name': 'studyplangroupsmodels', 'useList': True, 'type': 'StudyPlanGroupsModel'}, 'studyplanitemgroupmodels': {'name': 'studyplanitemgroupmodels', 'useList': True, 'type': 'StudyPlanItemGroupModel'}}}
    #{'name': 'id', 'type': 'graphene.String', 'column': 'id', 'isPrimaryKey': True}
    groups_by_id =  graphene.Field(
        'graphqltypes.gql_GroupModel.GroupModel', 
        id=graphene.String(required=True),
        resolver=gql_GroupModel.resolve_groups_by_id
    )
    #{'name': 'name', 'type': 'graphene.String', 'column': 'name', 'isPrimaryKey': False}
    groups_name_starts_with =  graphene.Field(
        'graphqltypes.gql_GroupModel.GroupModel', 
        name=graphene.String(required=True),
        resolver=gql_GroupModel.resolve_groups_name_starts_with
    )
    #{'name': 'abbreviation', 'type': 'graphene.String', 'column': 'abbreviation', 'isPrimaryKey': False}
    groups_abbreviation_starts_with =  graphene.Field(
        'graphqltypes.gql_GroupModel.GroupModel', 
        abbreviation=graphene.String(required=True),
        resolver=gql_GroupModel.resolve_groups_abbreviation_starts_with
    )
    #{'name': 'lastchange', 'type': 'graphene.DateTime', 'column': 'lastchange', 'isPrimaryKey': False}
    groups_lastchange_starts_with =  graphene.Field(
        'graphqltypes.gql_GroupModel.GroupModel', 
        lastchange=graphene.String(required=True),
        resolver=gql_GroupModel.resolve_groups_lastchange_starts_with
    )
    #{'name': 'entryYearId', 'type': 'graphene.Int', 'column': 'entryYearId', 'isPrimaryKey': False}
    groups_entryYearId_starts_with =  graphene.Field(
        'graphqltypes.gql_GroupModel.GroupModel', 
        entryYearId=graphene.String(required=True),
        resolver=gql_GroupModel.resolve_groups_entryYearId_starts_with
    )
    #{'name': 'externalId', 'type': 'graphene.String', 'column': 'externalId', 'isPrimaryKey': False}
    groups_externalId_starts_with =  graphene.Field(
        'graphqltypes.gql_GroupModel.GroupModel', 
        externalId=graphene.String(required=True),
        resolver=gql_GroupModel.resolve_groups_externalId_starts_with
    )
    #{'name': 'UIC', 'type': 'graphene.String', 'column': 'UIC', 'isPrimaryKey': False}
    groups_UIC_starts_with =  graphene.Field(
        'graphqltypes.gql_GroupModel.GroupModel', 
        UIC=graphene.String(required=True),
        resolver=gql_GroupModel.resolve_groups_UIC_starts_with
    )
    #{'name': 'grouptype_id', 'type': 'graphene.String', 'column': 'grouptype_id', 'isPrimaryKey': False}
    groups_grouptype_id_starts_with =  graphene.Field(
        'graphqltypes.gql_GroupModel.GroupModel', 
        grouptype_id=graphene.String(required=True),
        resolver=gql_GroupModel.resolve_groups_grouptype_id_starts_with
    )
    #{'SQLTableName': 'grouptypes', 'locals': {'id': {'name': 'id', 'type': 'graphene.String', 'column': 'id', 'isPrimaryKey': True}, 'name': {'name': 'name', 'type': 'graphene.String', 'column': 'name', 'isPrimaryKey': False}}, 'relations': {'groupmodels': {'name': 'groupmodels', 'useList': True, 'type': 'GroupModel'}}}
    #{'name': 'id', 'type': 'graphene.String', 'column': 'id', 'isPrimaryKey': True}
    grouptypes_by_id =  graphene.Field(
        'graphqltypes.gql_GroupTypeModel.GroupTypeModel', 
        id=graphene.String(required=True),
        resolver=gql_GroupTypeModel.resolve_grouptypes_by_id
    )
    #{'name': 'name', 'type': 'graphene.String', 'column': 'name', 'isPrimaryKey': False}
    grouptypes_name_starts_with =  graphene.Field(
        'graphqltypes.gql_GroupTypeModel.GroupTypeModel', 
        name=graphene.String(required=True),
        resolver=gql_GroupTypeModel.resolve_grouptypes_name_starts_with
    )
    #{'SQLTableName': 'programs', 'locals': {'id': {'name': 'id', 'type': 'graphene.String', 'column': 'id', 'isPrimaryKey': True}, 'name': {'name': 'name', 'type': 'graphene.String', 'column': 'name', 'isPrimaryKey': False}, 'lastchange': {'name': 'lastchange', 'type': 'graphene.DateTime', 'column': 'lastchange', 'isPrimaryKey': False}, 'externalId': {'name': 'externalId', 'type': 'graphene.Int', 'column': 'externalId', 'isPrimaryKey': False}}, 'relations': {'programusermodels': {'name': 'programusermodels', 'useList': True, 'type': 'ProgramUserModel'}, 'subjectmodels': {'name': 'subjectmodels', 'useList': True, 'type': 'SubjectModel'}}}
    #{'name': 'id', 'type': 'graphene.String', 'column': 'id', 'isPrimaryKey': True}
    programs_by_id =  graphene.Field(
        'graphqltypes.gql_ProgramModel.ProgramModel', 
        id=graphene.String(required=True),
        resolver=gql_ProgramModel.resolve_programs_by_id
    )
    #{'name': 'name', 'type': 'graphene.String', 'column': 'name', 'isPrimaryKey': False}
    programs_name_starts_with =  graphene.Field(
        'graphqltypes.gql_ProgramModel.ProgramModel', 
        name=graphene.String(required=True),
        resolver=gql_ProgramModel.resolve_programs_name_starts_with
    )
    #{'name': 'lastchange', 'type': 'graphene.DateTime', 'column': 'lastchange', 'isPrimaryKey': False}
    programs_lastchange_starts_with =  graphene.Field(
        'graphqltypes.gql_ProgramModel.ProgramModel', 
        lastchange=graphene.String(required=True),
        resolver=gql_ProgramModel.resolve_programs_lastchange_starts_with
    )
    #{'name': 'externalId', 'type': 'graphene.Int', 'column': 'externalId', 'isPrimaryKey': False}
    programs_externalId_starts_with =  graphene.Field(
        'graphqltypes.gql_ProgramModel.ProgramModel', 
        externalId=graphene.String(required=True),
        resolver=gql_ProgramModel.resolve_programs_externalId_starts_with
    )
    #{'SQLTableName': 'programs_users', 'locals': {'id': {'name': 'id', 'type': 'graphene.String', 'column': 'id', 'isPrimaryKey': True}, 'program_id': {'name': 'program_id', 'type': 'graphene.String', 'column': 'program_id', 'isPrimaryKey': False}, 'user_id': {'name': 'user_id', 'type': 'graphene.String', 'column': 'user_id', 'isPrimaryKey': False}, 'roletype_id': {'name': 'roletype_id', 'type': 'graphene.String', 'column': 'roletype_id', 'isPrimaryKey': False}}, 'relations': {'acreditationuserroletypemodel': {'name': 'acreditationuserroletypemodel', 'useList': False, 'type': 'AcreditationUserRoleTypeModel'}, 'programmodel': {'name': 'programmodel', 'useList': False, 'type': 'ProgramModel'}, 'usermodel': {'name': 'usermodel', 'useList': False, 'type': 'UserModel'}}}
    #{'name': 'id', 'type': 'graphene.String', 'column': 'id', 'isPrimaryKey': True}
    programs_users_by_id =  graphene.Field(
        'graphqltypes.gql_ProgramUserModel.ProgramUserModel', 
        id=graphene.String(required=True),
        resolver=gql_ProgramUserModel.resolve_programs_users_by_id
    )
    #{'name': 'program_id', 'type': 'graphene.String', 'column': 'program_id', 'isPrimaryKey': False}
    programs_users_program_id_starts_with =  graphene.Field(
        'graphqltypes.gql_ProgramUserModel.ProgramUserModel', 
        program_id=graphene.String(required=True),
        resolver=gql_ProgramUserModel.resolve_programs_users_program_id_starts_with
    )
    #{'name': 'user_id', 'type': 'graphene.String', 'column': 'user_id', 'isPrimaryKey': False}
    programs_users_user_id_starts_with =  graphene.Field(
        'graphqltypes.gql_ProgramUserModel.ProgramUserModel', 
        user_id=graphene.String(required=True),
        resolver=gql_ProgramUserModel.resolve_programs_users_user_id_starts_with
    )
    #{'name': 'roletype_id', 'type': 'graphene.String', 'column': 'roletype_id', 'isPrimaryKey': False}
    programs_users_roletype_id_starts_with =  graphene.Field(
        'graphqltypes.gql_ProgramUserModel.ProgramUserModel', 
        roletype_id=graphene.String(required=True),
        resolver=gql_ProgramUserModel.resolve_programs_users_roletype_id_starts_with
    )
    #{'SQLTableName': 'roles', 'locals': {'id': {'name': 'id', 'type': 'graphene.String', 'column': 'id', 'isPrimaryKey': True}, 'name': {'name': 'name', 'type': 'graphene.String', 'column': 'name', 'isPrimaryKey': False}, 'lastchange': {'name': 'lastchange', 'type': 'graphene.DateTime', 'column': 'lastchange', 'isPrimaryKey': False}, 'roletype_id': {'name': 'roletype_id', 'type': 'graphene.String', 'column': 'roletype_id', 'isPrimaryKey': False}, 'user_id': {'name': 'user_id', 'type': 'graphene.String', 'column': 'user_id', 'isPrimaryKey': False}, 'group_id': {'name': 'group_id', 'type': 'graphene.String', 'column': 'group_id', 'isPrimaryKey': False}}, 'relations': {'usermodel': {'name': 'usermodel', 'useList': False, 'type': 'UserModel'}, 'roletypemodel': {'name': 'roletypemodel', 'useList': False, 'type': 'RoleTypeModel'}, 'groupmodel': {'name': 'groupmodel', 'useList': False, 'type': 'GroupModel'}}}
    #{'name': 'id', 'type': 'graphene.String', 'column': 'id', 'isPrimaryKey': True}
    roles_by_id =  graphene.Field(
        'graphqltypes.gql_RoleModel.RoleModel', 
        id=graphene.String(required=True),
        resolver=gql_RoleModel.resolve_roles_by_id
    )
    #{'name': 'name', 'type': 'graphene.String', 'column': 'name', 'isPrimaryKey': False}
    roles_name_starts_with =  graphene.Field(
        'graphqltypes.gql_RoleModel.RoleModel', 
        name=graphene.String(required=True),
        resolver=gql_RoleModel.resolve_roles_name_starts_with
    )
    #{'name': 'lastchange', 'type': 'graphene.DateTime', 'column': 'lastchange', 'isPrimaryKey': False}
    roles_lastchange_starts_with =  graphene.Field(
        'graphqltypes.gql_RoleModel.RoleModel', 
        lastchange=graphene.String(required=True),
        resolver=gql_RoleModel.resolve_roles_lastchange_starts_with
    )
    #{'name': 'roletype_id', 'type': 'graphene.String', 'column': 'roletype_id', 'isPrimaryKey': False}
    roles_roletype_id_starts_with =  graphene.Field(
        'graphqltypes.gql_RoleModel.RoleModel', 
        roletype_id=graphene.String(required=True),
        resolver=gql_RoleModel.resolve_roles_roletype_id_starts_with
    )
    #{'name': 'user_id', 'type': 'graphene.String', 'column': 'user_id', 'isPrimaryKey': False}
    roles_user_id_starts_with =  graphene.Field(
        'graphqltypes.gql_RoleModel.RoleModel', 
        user_id=graphene.String(required=True),
        resolver=gql_RoleModel.resolve_roles_user_id_starts_with
    )
    #{'name': 'group_id', 'type': 'graphene.String', 'column': 'group_id', 'isPrimaryKey': False}
    roles_group_id_starts_with =  graphene.Field(
        'graphqltypes.gql_RoleModel.RoleModel', 
        group_id=graphene.String(required=True),
        resolver=gql_RoleModel.resolve_roles_group_id_starts_with
    )
    #{'SQLTableName': 'grouproletypes', 'locals': {'id': {'name': 'id', 'type': 'graphene.String', 'column': 'id', 'isPrimaryKey': True}, 'name': {'name': 'name', 'type': 'graphene.String', 'column': 'name', 'isPrimaryKey': False}}, 'relations': {'rolemodels': {'name': 'rolemodels', 'useList': True, 'type': 'RoleModel'}}}
    #{'name': 'id', 'type': 'graphene.String', 'column': 'id', 'isPrimaryKey': True}
    grouproletypes_by_id =  graphene.Field(
        'graphqltypes.gql_RoleTypeModel.RoleTypeModel', 
        id=graphene.String(required=True),
        resolver=gql_RoleTypeModel.resolve_grouproletypes_by_id
    )
    #{'name': 'name', 'type': 'graphene.String', 'column': 'name', 'isPrimaryKey': False}
    grouproletypes_name_starts_with =  graphene.Field(
        'graphqltypes.gql_RoleTypeModel.RoleTypeModel', 
        name=graphene.String(required=True),
        resolver=gql_RoleTypeModel.resolve_grouproletypes_name_starts_with
    )
    #{'SQLTableName': 'rooms', 'locals': {'id': {'name': 'id', 'type': 'graphene.String', 'column': 'id', 'isPrimaryKey': True}, 'name': {'name': 'name', 'type': 'graphene.String', 'column': 'name', 'isPrimaryKey': False}, 'lastchange': {'name': 'lastchange', 'type': 'graphene.DateTime', 'column': 'lastchange', 'isPrimaryKey': False}, 'externalId': {'name': 'externalId', 'type': 'graphene.String', 'column': 'externalId', 'isPrimaryKey': False}, 'building_id': {'name': 'building_id', 'type': 'graphene.String', 'column': 'building_id', 'isPrimaryKey': False}}, 'relations': {'buildingmodel': {'name': 'buildingmodel', 'useList': False, 'type': 'BuildingModel'}, 'eventroommodels': {'name': 'eventroommodels', 'useList': True, 'type': 'EventRoomModel'}}}
    #{'name': 'id', 'type': 'graphene.String', 'column': 'id', 'isPrimaryKey': True}
    rooms_by_id =  graphene.Field(
        'graphqltypes.gql_RoomModel.RoomModel', 
        id=graphene.String(required=True),
        resolver=gql_RoomModel.resolve_rooms_by_id
    )
    #{'name': 'name', 'type': 'graphene.String', 'column': 'name', 'isPrimaryKey': False}
    rooms_name_starts_with =  graphene.Field(
        'graphqltypes.gql_RoomModel.RoomModel', 
        name=graphene.String(required=True),
        resolver=gql_RoomModel.resolve_rooms_name_starts_with
    )
    #{'name': 'lastchange', 'type': 'graphene.DateTime', 'column': 'lastchange', 'isPrimaryKey': False}
    rooms_lastchange_starts_with =  graphene.Field(
        'graphqltypes.gql_RoomModel.RoomModel', 
        lastchange=graphene.String(required=True),
        resolver=gql_RoomModel.resolve_rooms_lastchange_starts_with
    )
    #{'name': 'externalId', 'type': 'graphene.String', 'column': 'externalId', 'isPrimaryKey': False}
    rooms_externalId_starts_with =  graphene.Field(
        'graphqltypes.gql_RoomModel.RoomModel', 
        externalId=graphene.String(required=True),
        resolver=gql_RoomModel.resolve_rooms_externalId_starts_with
    )
    #{'name': 'building_id', 'type': 'graphene.String', 'column': 'building_id', 'isPrimaryKey': False}
    rooms_building_id_starts_with =  graphene.Field(
        'graphqltypes.gql_RoomModel.RoomModel', 
        building_id=graphene.String(required=True),
        resolver=gql_RoomModel.resolve_rooms_building_id_starts_with
    )
    #{'SQLTableName': 'studyplans_groups', 'locals': {'id': {'name': 'id', 'type': 'graphene.String', 'column': 'id', 'isPrimaryKey': True}, 'studyplan_id': {'name': 'studyplan_id', 'type': 'graphene.String', 'column': 'studyplan_id', 'isPrimaryKey': False}, 'group_id': {'name': 'group_id', 'type': 'graphene.String', 'column': 'group_id', 'isPrimaryKey': False}}, 'relations': {'groupmodel': {'name': 'groupmodel', 'useList': False, 'type': 'GroupModel'}, 'studyplanmodel': {'name': 'studyplanmodel', 'useList': False, 'type': 'StudyPlanModel'}}}
    #{'name': 'id', 'type': 'graphene.String', 'column': 'id', 'isPrimaryKey': True}
    studyplans_groups_by_id =  graphene.Field(
        'graphqltypes.gql_StudyPlanGroupsModel.StudyPlanGroupsModel', 
        id=graphene.String(required=True),
        resolver=gql_StudyPlanGroupsModel.resolve_studyplans_groups_by_id
    )
    #{'name': 'studyplan_id', 'type': 'graphene.String', 'column': 'studyplan_id', 'isPrimaryKey': False}
    studyplans_groups_studyplan_id_starts_with =  graphene.Field(
        'graphqltypes.gql_StudyPlanGroupsModel.StudyPlanGroupsModel', 
        studyplan_id=graphene.String(required=True),
        resolver=gql_StudyPlanGroupsModel.resolve_studyplans_groups_studyplan_id_starts_with
    )
    #{'name': 'group_id', 'type': 'graphene.String', 'column': 'group_id', 'isPrimaryKey': False}
    studyplans_groups_group_id_starts_with =  graphene.Field(
        'graphqltypes.gql_StudyPlanGroupsModel.StudyPlanGroupsModel', 
        group_id=graphene.String(required=True),
        resolver=gql_StudyPlanGroupsModel.resolve_studyplans_groups_group_id_starts_with
    )
    #{'SQLTableName': 'studyplanitem_events', 'locals': {'id': {'name': 'id', 'type': 'graphene.String', 'column': 'id', 'isPrimaryKey': True}, 'studyplanitem_id': {'name': 'studyplanitem_id', 'type': 'graphene.String', 'column': 'studyplanitem_id', 'isPrimaryKey': False}, 'event_id': {'name': 'event_id', 'type': 'graphene.String', 'column': 'event_id', 'isPrimaryKey': False}}, 'relations': {'eventmodel': {'name': 'eventmodel', 'useList': False, 'type': 'EventModel'}, 'studyplanitemmodel': {'name': 'studyplanitemmodel', 'useList': False, 'type': 'StudyPlanItemModel'}}}
    #{'name': 'id', 'type': 'graphene.String', 'column': 'id', 'isPrimaryKey': True}
    studyplanitem_events_by_id =  graphene.Field(
        'graphqltypes.gql_StudyPlanItemEventModel.StudyPlanItemEventModel', 
        id=graphene.String(required=True),
        resolver=gql_StudyPlanItemEventModel.resolve_studyplanitem_events_by_id
    )
    #{'name': 'studyplanitem_id', 'type': 'graphene.String', 'column': 'studyplanitem_id', 'isPrimaryKey': False}
    studyplanitem_events_studyplanitem_id_starts_with =  graphene.Field(
        'graphqltypes.gql_StudyPlanItemEventModel.StudyPlanItemEventModel', 
        studyplanitem_id=graphene.String(required=True),
        resolver=gql_StudyPlanItemEventModel.resolve_studyplanitem_events_studyplanitem_id_starts_with
    )
    #{'name': 'event_id', 'type': 'graphene.String', 'column': 'event_id', 'isPrimaryKey': False}
    studyplanitem_events_event_id_starts_with =  graphene.Field(
        'graphqltypes.gql_StudyPlanItemEventModel.StudyPlanItemEventModel', 
        event_id=graphene.String(required=True),
        resolver=gql_StudyPlanItemEventModel.resolve_studyplanitem_events_event_id_starts_with
    )
    #{'SQLTableName': 'studyplanitem_groups', 'locals': {'id': {'name': 'id', 'type': 'graphene.String', 'column': 'id', 'isPrimaryKey': True}, 'group_id': {'name': 'group_id', 'type': 'graphene.String', 'column': 'group_id', 'isPrimaryKey': False}, 'studyplanitem_id': {'name': 'studyplanitem_id', 'type': 'graphene.String', 'column': 'studyplanitem_id', 'isPrimaryKey': False}}, 'relations': {'studyplanitemmodel': {'name': 'studyplanitemmodel', 'useList': False, 'type': 'StudyPlanItemModel'}, 'groupmodel': {'name': 'groupmodel', 'useList': False, 'type': 'GroupModel'}}}
    #{'name': 'id', 'type': 'graphene.String', 'column': 'id', 'isPrimaryKey': True}
    studyplanitem_groups_by_id =  graphene.Field(
        'graphqltypes.gql_StudyPlanItemGroupModel.StudyPlanItemGroupModel', 
        id=graphene.String(required=True),
        resolver=gql_StudyPlanItemGroupModel.resolve_studyplanitem_groups_by_id
    )
    #{'name': 'group_id', 'type': 'graphene.String', 'column': 'group_id', 'isPrimaryKey': False}
    studyplanitem_groups_group_id_starts_with =  graphene.Field(
        'graphqltypes.gql_StudyPlanItemGroupModel.StudyPlanItemGroupModel', 
        group_id=graphene.String(required=True),
        resolver=gql_StudyPlanItemGroupModel.resolve_studyplanitem_groups_group_id_starts_with
    )
    #{'name': 'studyplanitem_id', 'type': 'graphene.String', 'column': 'studyplanitem_id', 'isPrimaryKey': False}
    studyplanitem_groups_studyplanitem_id_starts_with =  graphene.Field(
        'graphqltypes.gql_StudyPlanItemGroupModel.StudyPlanItemGroupModel', 
        studyplanitem_id=graphene.String(required=True),
        resolver=gql_StudyPlanItemGroupModel.resolve_studyplanitem_groups_studyplanitem_id_starts_with
    )
    #{'SQLTableName': 'studyplanitems', 'locals': {'id': {'name': 'id', 'type': 'graphene.String', 'column': 'id', 'isPrimaryKey': True}, 'name': {'name': 'name', 'type': 'graphene.String', 'column': 'name', 'isPrimaryKey': False}, 'priority': {'name': 'priority', 'type': 'graphene.Int', 'column': 'priority', 'isPrimaryKey': False}, 'subjectSemesterTopic': {'name': 'subjectSemesterTopic', 'type': 'graphene.String', 'column': 'subjectSemesterTopic', 'isPrimaryKey': False}, 'externalId': {'name': 'externalId', 'type': 'graphene.String', 'column': 'externalId', 'isPrimaryKey': False}, 'studyplan_id': {'name': 'studyplan_id', 'type': 'graphene.String', 'column': 'studyplan_id', 'isPrimaryKey': False}}, 'relations': {'studyplanmodel': {'name': 'studyplanmodel', 'useList': False, 'type': 'StudyPlanModel'}, 'studyplanitemeventmodels': {'name': 'studyplanitemeventmodels', 'useList': True, 'type': 'StudyPlanItemEventModel'}, 'studyplanitemteachermodels': {'name': 'studyplanitemteachermodels', 'useList': True, 'type': 'StudyPlanItemTeacherModel'}, 'studyplanitemgroupmodels': {'name': 'studyplanitemgroupmodels', 'useList': True, 'type': 'StudyPlanItemGroupModel'}}}
    #{'name': 'id', 'type': 'graphene.String', 'column': 'id', 'isPrimaryKey': True}
    studyplanitems_by_id =  graphene.Field(
        'graphqltypes.gql_StudyPlanItemModel.StudyPlanItemModel', 
        id=graphene.String(required=True),
        resolver=gql_StudyPlanItemModel.resolve_studyplanitems_by_id
    )
    #{'name': 'name', 'type': 'graphene.String', 'column': 'name', 'isPrimaryKey': False}
    studyplanitems_name_starts_with =  graphene.Field(
        'graphqltypes.gql_StudyPlanItemModel.StudyPlanItemModel', 
        name=graphene.String(required=True),
        resolver=gql_StudyPlanItemModel.resolve_studyplanitems_name_starts_with
    )
    #{'name': 'priority', 'type': 'graphene.Int', 'column': 'priority', 'isPrimaryKey': False}
    studyplanitems_priority_starts_with =  graphene.Field(
        'graphqltypes.gql_StudyPlanItemModel.StudyPlanItemModel', 
        priority=graphene.String(required=True),
        resolver=gql_StudyPlanItemModel.resolve_studyplanitems_priority_starts_with
    )
    #{'name': 'subjectSemesterTopic', 'type': 'graphene.String', 'column': 'subjectSemesterTopic', 'isPrimaryKey': False}
    studyplanitems_subjectSemesterTopic_starts_with =  graphene.Field(
        'graphqltypes.gql_StudyPlanItemModel.StudyPlanItemModel', 
        subjectSemesterTopic=graphene.String(required=True),
        resolver=gql_StudyPlanItemModel.resolve_studyplanitems_subjectSemesterTopic_starts_with
    )
    #{'name': 'externalId', 'type': 'graphene.String', 'column': 'externalId', 'isPrimaryKey': False}
    studyplanitems_externalId_starts_with =  graphene.Field(
        'graphqltypes.gql_StudyPlanItemModel.StudyPlanItemModel', 
        externalId=graphene.String(required=True),
        resolver=gql_StudyPlanItemModel.resolve_studyplanitems_externalId_starts_with
    )
    #{'name': 'studyplan_id', 'type': 'graphene.String', 'column': 'studyplan_id', 'isPrimaryKey': False}
    studyplanitems_studyplan_id_starts_with =  graphene.Field(
        'graphqltypes.gql_StudyPlanItemModel.StudyPlanItemModel', 
        studyplan_id=graphene.String(required=True),
        resolver=gql_StudyPlanItemModel.resolve_studyplanitems_studyplan_id_starts_with
    )
    #{'SQLTableName': 'studyplanitem_teachers', 'locals': {'id': {'name': 'id', 'type': 'graphene.String', 'column': 'id', 'isPrimaryKey': True}, 'teacher_id': {'name': 'teacher_id', 'type': 'graphene.String', 'column': 'teacher_id', 'isPrimaryKey': False}, 'studyplanitem_id': {'name': 'studyplanitem_id', 'type': 'graphene.String', 'column': 'studyplanitem_id', 'isPrimaryKey': False}}, 'relations': {'studyplanitemmodel': {'name': 'studyplanitemmodel', 'useList': False, 'type': 'StudyPlanItemModel'}, 'usermodel': {'name': 'usermodel', 'useList': False, 'type': 'UserModel'}}}
    #{'name': 'id', 'type': 'graphene.String', 'column': 'id', 'isPrimaryKey': True}
    studyplanitem_teachers_by_id =  graphene.Field(
        'graphqltypes.gql_StudyPlanItemTeacherModel.StudyPlanItemTeacherModel', 
        id=graphene.String(required=True),
        resolver=gql_StudyPlanItemTeacherModel.resolve_studyplanitem_teachers_by_id
    )
    #{'name': 'teacher_id', 'type': 'graphene.String', 'column': 'teacher_id', 'isPrimaryKey': False}
    studyplanitem_teachers_teacher_id_starts_with =  graphene.Field(
        'graphqltypes.gql_StudyPlanItemTeacherModel.StudyPlanItemTeacherModel', 
        teacher_id=graphene.String(required=True),
        resolver=gql_StudyPlanItemTeacherModel.resolve_studyplanitem_teachers_teacher_id_starts_with
    )
    #{'name': 'studyplanitem_id', 'type': 'graphene.String', 'column': 'studyplanitem_id', 'isPrimaryKey': False}
    studyplanitem_teachers_studyplanitem_id_starts_with =  graphene.Field(
        'graphqltypes.gql_StudyPlanItemTeacherModel.StudyPlanItemTeacherModel', 
        studyplanitem_id=graphene.String(required=True),
        resolver=gql_StudyPlanItemTeacherModel.resolve_studyplanitem_teachers_studyplanitem_id_starts_with
    )
    #{'SQLTableName': 'studyplans', 'locals': {'id': {'name': 'id', 'type': 'graphene.String', 'column': 'id', 'isPrimaryKey': True}, 'name': {'name': 'name', 'type': 'graphene.String', 'column': 'name', 'isPrimaryKey': False}, 'externalId': {'name': 'externalId', 'type': 'graphene.String', 'column': 'externalId', 'isPrimaryKey': False}}, 'relations': {'studyplanitemmodels': {'name': 'studyplanitemmodels', 'useList': True, 'type': 'StudyPlanItemModel'}, 'studyplangroupsmodels': {'name': 'studyplangroupsmodels', 'useList': True, 'type': 'StudyPlanGroupsModel'}}}
    #{'name': 'id', 'type': 'graphene.String', 'column': 'id', 'isPrimaryKey': True}
    studyplans_by_id =  graphene.Field(
        'graphqltypes.gql_StudyPlanModel.StudyPlanModel', 
        id=graphene.String(required=True),
        resolver=gql_StudyPlanModel.resolve_studyplans_by_id
    )
    #{'name': 'name', 'type': 'graphene.String', 'column': 'name', 'isPrimaryKey': False}
    studyplans_name_starts_with =  graphene.Field(
        'graphqltypes.gql_StudyPlanModel.StudyPlanModel', 
        name=graphene.String(required=True),
        resolver=gql_StudyPlanModel.resolve_studyplans_name_starts_with
    )
    #{'name': 'externalId', 'type': 'graphene.String', 'column': 'externalId', 'isPrimaryKey': False}
    studyplans_externalId_starts_with =  graphene.Field(
        'graphqltypes.gql_StudyPlanModel.StudyPlanModel', 
        externalId=graphene.String(required=True),
        resolver=gql_StudyPlanModel.resolve_studyplans_externalId_starts_with
    )
    #{'SQLTableName': 'subjects', 'locals': {'id': {'name': 'id', 'type': 'graphene.String', 'column': 'id', 'isPrimaryKey': True}, 'name': {'name': 'name', 'type': 'graphene.String', 'column': 'name', 'isPrimaryKey': False}, 'lastchange': {'name': 'lastchange', 'type': 'graphene.DateTime', 'column': 'lastchange', 'isPrimaryKey': False}, 'externalId': {'name': 'externalId', 'type': 'graphene.String', 'column': 'externalId', 'isPrimaryKey': False}, 'program_id': {'name': 'program_id', 'type': 'graphene.String', 'column': 'program_id', 'isPrimaryKey': False}}, 'relations': {'programmodel': {'name': 'programmodel', 'useList': False, 'type': 'ProgramModel'}, 'subjectusermodels': {'name': 'subjectusermodels', 'useList': True, 'type': 'SubjectUserModel'}, 'subjectsemestermodels': {'name': 'subjectsemestermodels', 'useList': True, 'type': 'SubjectSemesterModel'}}}
    #{'name': 'id', 'type': 'graphene.String', 'column': 'id', 'isPrimaryKey': True}
    subjects_by_id =  graphene.Field(
        'graphqltypes.gql_SubjectModel.SubjectModel', 
        id=graphene.String(required=True),
        resolver=gql_SubjectModel.resolve_subjects_by_id
    )
    #{'name': 'name', 'type': 'graphene.String', 'column': 'name', 'isPrimaryKey': False}
    subjects_name_starts_with =  graphene.Field(
        'graphqltypes.gql_SubjectModel.SubjectModel', 
        name=graphene.String(required=True),
        resolver=gql_SubjectModel.resolve_subjects_name_starts_with
    )
    #{'name': 'lastchange', 'type': 'graphene.DateTime', 'column': 'lastchange', 'isPrimaryKey': False}
    subjects_lastchange_starts_with =  graphene.Field(
        'graphqltypes.gql_SubjectModel.SubjectModel', 
        lastchange=graphene.String(required=True),
        resolver=gql_SubjectModel.resolve_subjects_lastchange_starts_with
    )
    #{'name': 'externalId', 'type': 'graphene.String', 'column': 'externalId', 'isPrimaryKey': False}
    subjects_externalId_starts_with =  graphene.Field(
        'graphqltypes.gql_SubjectModel.SubjectModel', 
        externalId=graphene.String(required=True),
        resolver=gql_SubjectModel.resolve_subjects_externalId_starts_with
    )
    #{'name': 'program_id', 'type': 'graphene.String', 'column': 'program_id', 'isPrimaryKey': False}
    subjects_program_id_starts_with =  graphene.Field(
        'graphqltypes.gql_SubjectModel.SubjectModel', 
        program_id=graphene.String(required=True),
        resolver=gql_SubjectModel.resolve_subjects_program_id_starts_with
    )
    #{'SQLTableName': 'subjectsemesters', 'locals': {'id': {'name': 'id', 'type': 'graphene.String', 'column': 'id', 'isPrimaryKey': True}, 'name': {'name': 'name', 'type': 'graphene.String', 'column': 'name', 'isPrimaryKey': False}, 'lastchange': {'name': 'lastchange', 'type': 'graphene.DateTime', 'column': 'lastchange', 'isPrimaryKey': False}, 'subject_id': {'name': 'subject_id', 'type': 'graphene.String', 'column': 'subject_id', 'isPrimaryKey': False}}, 'relations': {'subjectmodel': {'name': 'subjectmodel', 'useList': False, 'type': 'SubjectModel'}, 'subjecttopicmodels': {'name': 'subjecttopicmodels', 'useList': True, 'type': 'SubjectTopicModel'}}}
    #{'name': 'id', 'type': 'graphene.String', 'column': 'id', 'isPrimaryKey': True}
    subjectsemesters_by_id =  graphene.Field(
        'graphqltypes.gql_SubjectSemesterModel.SubjectSemesterModel', 
        id=graphene.String(required=True),
        resolver=gql_SubjectSemesterModel.resolve_subjectsemesters_by_id
    )
    #{'name': 'name', 'type': 'graphene.String', 'column': 'name', 'isPrimaryKey': False}
    subjectsemesters_name_starts_with =  graphene.Field(
        'graphqltypes.gql_SubjectSemesterModel.SubjectSemesterModel', 
        name=graphene.String(required=True),
        resolver=gql_SubjectSemesterModel.resolve_subjectsemesters_name_starts_with
    )
    #{'name': 'lastchange', 'type': 'graphene.DateTime', 'column': 'lastchange', 'isPrimaryKey': False}
    subjectsemesters_lastchange_starts_with =  graphene.Field(
        'graphqltypes.gql_SubjectSemesterModel.SubjectSemesterModel', 
        lastchange=graphene.String(required=True),
        resolver=gql_SubjectSemesterModel.resolve_subjectsemesters_lastchange_starts_with
    )
    #{'name': 'subject_id', 'type': 'graphene.String', 'column': 'subject_id', 'isPrimaryKey': False}
    subjectsemesters_subject_id_starts_with =  graphene.Field(
        'graphqltypes.gql_SubjectSemesterModel.SubjectSemesterModel', 
        subject_id=graphene.String(required=True),
        resolver=gql_SubjectSemesterModel.resolve_subjectsemesters_subject_id_starts_with
    )
    #{'SQLTableName': 'subjecttopics', 'locals': {'id': {'name': 'id', 'type': 'graphene.String', 'column': 'id', 'isPrimaryKey': True}, 'name': {'name': 'name', 'type': 'graphene.String', 'column': 'name', 'isPrimaryKey': False}, 'externalId': {'name': 'externalId', 'type': 'graphene.String', 'column': 'externalId', 'isPrimaryKey': False}, 'subjectsemester_id': {'name': 'subjectsemester_id', 'type': 'graphene.String', 'column': 'subjectsemester_id', 'isPrimaryKey': False}}, 'relations': {'subjectsemestermodel': {'name': 'subjectsemestermodel', 'useList': False, 'type': 'SubjectSemesterModel'}, 'subjecttopicusermodels': {'name': 'subjecttopicusermodels', 'useList': True, 'type': 'SubjectTopicUserModel'}}}
    #{'name': 'id', 'type': 'graphene.String', 'column': 'id', 'isPrimaryKey': True}
    subjecttopics_by_id =  graphene.Field(
        'graphqltypes.gql_SubjectTopicModel.SubjectTopicModel', 
        id=graphene.String(required=True),
        resolver=gql_SubjectTopicModel.resolve_subjecttopics_by_id
    )
    #{'name': 'name', 'type': 'graphene.String', 'column': 'name', 'isPrimaryKey': False}
    subjecttopics_name_starts_with =  graphene.Field(
        'graphqltypes.gql_SubjectTopicModel.SubjectTopicModel', 
        name=graphene.String(required=True),
        resolver=gql_SubjectTopicModel.resolve_subjecttopics_name_starts_with
    )
    #{'name': 'externalId', 'type': 'graphene.String', 'column': 'externalId', 'isPrimaryKey': False}
    subjecttopics_externalId_starts_with =  graphene.Field(
        'graphqltypes.gql_SubjectTopicModel.SubjectTopicModel', 
        externalId=graphene.String(required=True),
        resolver=gql_SubjectTopicModel.resolve_subjecttopics_externalId_starts_with
    )
    #{'name': 'subjectsemester_id', 'type': 'graphene.String', 'column': 'subjectsemester_id', 'isPrimaryKey': False}
    subjecttopics_subjectsemester_id_starts_with =  graphene.Field(
        'graphqltypes.gql_SubjectTopicModel.SubjectTopicModel', 
        subjectsemester_id=graphene.String(required=True),
        resolver=gql_SubjectTopicModel.resolve_subjecttopics_subjectsemester_id_starts_with
    )
    #{'SQLTableName': 'subjecttopics_users', 'locals': {'id': {'name': 'id', 'type': 'graphene.String', 'column': 'id', 'isPrimaryKey': True}, 'subjecttopic_id': {'name': 'subjecttopic_id', 'type': 'graphene.String', 'column': 'subjecttopic_id', 'isPrimaryKey': False}, 'user_id': {'name': 'user_id', 'type': 'graphene.String', 'column': 'user_id', 'isPrimaryKey': False}, 'roletype_id': {'name': 'roletype_id', 'type': 'graphene.String', 'column': 'roletype_id', 'isPrimaryKey': False}}, 'relations': {'subjecttopicmodel': {'name': 'subjecttopicmodel', 'useList': False, 'type': 'SubjectTopicModel'}, 'usermodel': {'name': 'usermodel', 'useList': False, 'type': 'UserModel'}, 'acreditationuserroletypemodel': {'name': 'acreditationuserroletypemodel', 'useList': False, 'type': 'AcreditationUserRoleTypeModel'}}}
    #{'name': 'id', 'type': 'graphene.String', 'column': 'id', 'isPrimaryKey': True}
    subjecttopics_users_by_id =  graphene.Field(
        'graphqltypes.gql_SubjectTopicUserModel.SubjectTopicUserModel', 
        id=graphene.String(required=True),
        resolver=gql_SubjectTopicUserModel.resolve_subjecttopics_users_by_id
    )
    #{'name': 'subjecttopic_id', 'type': 'graphene.String', 'column': 'subjecttopic_id', 'isPrimaryKey': False}
    subjecttopics_users_subjecttopic_id_starts_with =  graphene.Field(
        'graphqltypes.gql_SubjectTopicUserModel.SubjectTopicUserModel', 
        subjecttopic_id=graphene.String(required=True),
        resolver=gql_SubjectTopicUserModel.resolve_subjecttopics_users_subjecttopic_id_starts_with
    )
    #{'name': 'user_id', 'type': 'graphene.String', 'column': 'user_id', 'isPrimaryKey': False}
    subjecttopics_users_user_id_starts_with =  graphene.Field(
        'graphqltypes.gql_SubjectTopicUserModel.SubjectTopicUserModel', 
        user_id=graphene.String(required=True),
        resolver=gql_SubjectTopicUserModel.resolve_subjecttopics_users_user_id_starts_with
    )
    #{'name': 'roletype_id', 'type': 'graphene.String', 'column': 'roletype_id', 'isPrimaryKey': False}
    subjecttopics_users_roletype_id_starts_with =  graphene.Field(
        'graphqltypes.gql_SubjectTopicUserModel.SubjectTopicUserModel', 
        roletype_id=graphene.String(required=True),
        resolver=gql_SubjectTopicUserModel.resolve_subjecttopics_users_roletype_id_starts_with
    )
    #{'SQLTableName': 'subjects_users', 'locals': {'id': {'name': 'id', 'type': 'graphene.String', 'column': 'id', 'isPrimaryKey': True}, 'subject_id': {'name': 'subject_id', 'type': 'graphene.String', 'column': 'subject_id', 'isPrimaryKey': False}, 'user_id': {'name': 'user_id', 'type': 'graphene.String', 'column': 'user_id', 'isPrimaryKey': False}, 'roletype_id': {'name': 'roletype_id', 'type': 'graphene.String', 'column': 'roletype_id', 'isPrimaryKey': False}}, 'relations': {'usermodel': {'name': 'usermodel', 'useList': False, 'type': 'UserModel'}, 'subjectmodel': {'name': 'subjectmodel', 'useList': False, 'type': 'SubjectModel'}, 'acreditationuserroletypemodel': {'name': 'acreditationuserroletypemodel', 'useList': False, 'type': 'AcreditationUserRoleTypeModel'}}}
    #{'name': 'id', 'type': 'graphene.String', 'column': 'id', 'isPrimaryKey': True}
    subjects_users_by_id =  graphene.Field(
        'graphqltypes.gql_SubjectUserModel.SubjectUserModel', 
        id=graphene.String(required=True),
        resolver=gql_SubjectUserModel.resolve_subjects_users_by_id
    )
    #{'name': 'subject_id', 'type': 'graphene.String', 'column': 'subject_id', 'isPrimaryKey': False}
    subjects_users_subject_id_starts_with =  graphene.Field(
        'graphqltypes.gql_SubjectUserModel.SubjectUserModel', 
        subject_id=graphene.String(required=True),
        resolver=gql_SubjectUserModel.resolve_subjects_users_subject_id_starts_with
    )
    #{'name': 'user_id', 'type': 'graphene.String', 'column': 'user_id', 'isPrimaryKey': False}
    subjects_users_user_id_starts_with =  graphene.Field(
        'graphqltypes.gql_SubjectUserModel.SubjectUserModel', 
        user_id=graphene.String(required=True),
        resolver=gql_SubjectUserModel.resolve_subjects_users_user_id_starts_with
    )
    #{'name': 'roletype_id', 'type': 'graphene.String', 'column': 'roletype_id', 'isPrimaryKey': False}
    subjects_users_roletype_id_starts_with =  graphene.Field(
        'graphqltypes.gql_SubjectUserModel.SubjectUserModel', 
        roletype_id=graphene.String(required=True),
        resolver=gql_SubjectUserModel.resolve_subjects_users_roletype_id_starts_with
    )
    #{'SQLTableName': 'users_groups', 'locals': {'id': {'name': 'id', 'type': 'graphene.String', 'column': 'id', 'isPrimaryKey': True}, 'user_id': {'name': 'user_id', 'type': 'graphene.String', 'column': 'user_id', 'isPrimaryKey': False}, 'group_id': {'name': 'group_id', 'type': 'graphene.String', 'column': 'group_id', 'isPrimaryKey': False}}, 'relations': {'usermodel': {'name': 'usermodel', 'useList': False, 'type': 'UserModel'}, 'groupmodel': {'name': 'groupmodel', 'useList': False, 'type': 'GroupModel'}}}
    #{'name': 'id', 'type': 'graphene.String', 'column': 'id', 'isPrimaryKey': True}
    users_groups_by_id =  graphene.Field(
        'graphqltypes.gql_UserGroupModel.UserGroupModel', 
        id=graphene.String(required=True),
        resolver=gql_UserGroupModel.resolve_users_groups_by_id
    )
    #{'name': 'user_id', 'type': 'graphene.String', 'column': 'user_id', 'isPrimaryKey': False}
    users_groups_user_id_starts_with =  graphene.Field(
        'graphqltypes.gql_UserGroupModel.UserGroupModel', 
        user_id=graphene.String(required=True),
        resolver=gql_UserGroupModel.resolve_users_groups_user_id_starts_with
    )
    #{'name': 'group_id', 'type': 'graphene.String', 'column': 'group_id', 'isPrimaryKey': False}
    users_groups_group_id_starts_with =  graphene.Field(
        'graphqltypes.gql_UserGroupModel.UserGroupModel', 
        group_id=graphene.String(required=True),
        resolver=gql_UserGroupModel.resolve_users_groups_group_id_starts_with
    )
    #{'SQLTableName': 'users', 'locals': {'id': {'name': 'id', 'type': 'graphene.String', 'column': 'id', 'isPrimaryKey': True}, 'name': {'name': 'name', 'type': 'graphene.String', 'column': 'name', 'isPrimaryKey': False}, 'surname': {'name': 'surname', 'type': 'graphene.String', 'column': 'surname', 'isPrimaryKey': False}, 'email': {'name': 'email', 'type': 'graphene.String', 'column': 'email', 'isPrimaryKey': False}, 'lastchange': {'name': 'lastchange', 'type': 'graphene.DateTime', 'column': 'lastchange', 'isPrimaryKey': False}, 'externalId': {'name': 'externalId', 'type': 'graphene.Int', 'column': 'externalId', 'isPrimaryKey': False}, 'UCO': {'name': 'UCO', 'type': 'graphene.String', 'column': 'UCO', 'isPrimaryKey': False}, 'VaVId': {'name': 'VaVId', 'type': 'graphene.String', 'column': 'VaVId', 'isPrimaryKey': False}}, 'relations': {'eventusermodels': {'name': 'eventusermodels', 'useList': True, 'type': 'EventUserModel'}, 'programusermodels': {'name': 'programusermodels', 'useList': True, 'type': 'ProgramUserModel'}, 'usergroupmodels': {'name': 'usergroupmodels', 'useList': True, 'type': 'UserGroupModel'}, 'rolemodels': {'name': 'rolemodels', 'useList': True, 'type': 'RoleModel'}, 'subjectusermodels': {'name': 'subjectusermodels', 'useList': True, 'type': 'SubjectUserModel'}, 'studyplanitemteachermodels': {'name': 'studyplanitemteachermodels', 'useList': True, 'type': 'StudyPlanItemTeacherModel'}, 'subjecttopicusermodels': {'name': 'subjecttopicusermodels', 'useList': True, 'type': 'SubjectTopicUserModel'}}}
    #{'name': 'id', 'type': 'graphene.String', 'column': 'id', 'isPrimaryKey': True}
    users_by_id =  graphene.Field(
        'graphqltypes.gql_UserModel.UserModel', 
        id=graphene.String(required=True),
        resolver=gql_UserModel.resolve_users_by_id
    )
    #{'name': 'name', 'type': 'graphene.String', 'column': 'name', 'isPrimaryKey': False}
    users_name_starts_with =  graphene.Field(
        'graphqltypes.gql_UserModel.UserModel', 
        name=graphene.String(required=True),
        resolver=gql_UserModel.resolve_users_name_starts_with
    )
    #{'name': 'surname', 'type': 'graphene.String', 'column': 'surname', 'isPrimaryKey': False}
    users_surname_starts_with =  graphene.Field(
        'graphqltypes.gql_UserModel.UserModel', 
        surname=graphene.String(required=True),
        resolver=gql_UserModel.resolve_users_surname_starts_with
    )
    #{'name': 'email', 'type': 'graphene.String', 'column': 'email', 'isPrimaryKey': False}
    users_email_starts_with =  graphene.Field(
        'graphqltypes.gql_UserModel.UserModel', 
        email=graphene.String(required=True),
        resolver=gql_UserModel.resolve_users_email_starts_with
    )
    #{'name': 'lastchange', 'type': 'graphene.DateTime', 'column': 'lastchange', 'isPrimaryKey': False}
    users_lastchange_starts_with =  graphene.Field(
        'graphqltypes.gql_UserModel.UserModel', 
        lastchange=graphene.String(required=True),
        resolver=gql_UserModel.resolve_users_lastchange_starts_with
    )
    #{'name': 'externalId', 'type': 'graphene.Int', 'column': 'externalId', 'isPrimaryKey': False}
    users_externalId_starts_with =  graphene.Field(
        'graphqltypes.gql_UserModel.UserModel', 
        externalId=graphene.String(required=True),
        resolver=gql_UserModel.resolve_users_externalId_starts_with
    )
    #{'name': 'UCO', 'type': 'graphene.String', 'column': 'UCO', 'isPrimaryKey': False}
    users_UCO_starts_with =  graphene.Field(
        'graphqltypes.gql_UserModel.UserModel', 
        UCO=graphene.String(required=True),
        resolver=gql_UserModel.resolve_users_UCO_starts_with
    )
    #{'name': 'VaVId', 'type': 'graphene.String', 'column': 'VaVId', 'isPrimaryKey': False}
    users_VaVId_starts_with =  graphene.Field(
        'graphqltypes.gql_UserModel.UserModel', 
        VaVId=graphene.String(required=True),
        resolver=gql_UserModel.resolve_users_VaVId_starts_with
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