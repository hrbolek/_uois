from uoishelpers.dataloaders import createIdLoader, createFkeyLoader
from functools import cache

from gql_facilities.DBDefinitions import FacilityModel, FacilityTypeModel
#from gql_facilities.DBDefinitions import FacilityManagement
from gql_facilities.DBDefinitions import EventFacilityModel, EventFacilityStateType

async def createLoaders_3(asyncSessionMaker):

    class Loaders:
        @property
        @cache
        def facility_by_id(self):
            return createIdLoader(asyncSessionMaker, FacilityModel)

        @property
        @cache
        def facilities(self):
            return createIdLoader(asyncSessionMaker, FacilityModel)

        @property
        @cache
        def facilitytype_by_id(self):
            return createIdLoader(asyncSessionMaker, FacilityTypeModel)

        @property
        @cache
        def facilities_by_master_id(self):
            return createFkeyLoader(asyncSessionMaker, FacilityModel, foreignKeyName="master_facility_id")

        @property
        @cache
        def facilities_by_group_id(self):
            return createFkeyLoader(asyncSessionMaker, FacilityModel, foreignKeyName="group_id")

        @property
        @cache
        def event_facility_by_facility_id(self):
            return createFkeyLoader(asyncSessionMaker, EventFacilityModel, foreignKeyName="facility_id")

        @property
        @cache
        def event_facility_by_id(self):
            return createIdLoader(asyncSessionMaker, EventFacilityModel)

        @property
        @cache
        def event_facility_state_by_id(self):
            return createIdLoader(asyncSessionMaker, EventFacilityStateType)

        @property
        @cache
        def facilitysubs_by_master_facility_id(self):
            return createFkeyLoader(asyncSessionMaker, FacilityModel, foreignKeyName="master_facility_id")

        # @property
        # @cache
        # def facilitymanagement(self):
        #     return createIdLoader(asyncSessionMaker, FacilityManagement)

    return Loaders()
