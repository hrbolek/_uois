from uoishelpers.dataloaders import createIdLoader, createFkeyLoader
from functools import cache

from gql_forms.DBDefinitions import FormModel, FormTypeModel, FormCategoryModel
from gql_forms.DBDefinitions import RequestModel, HistoryModel
from gql_forms.DBDefinitions import SectionModel, PartModel
from gql_forms.DBDefinitions import ItemModel, ItemTypeModel, ItemCategoryModel

async def createLoaders_3(asyncSessionMaker):

    class Loaders:
        @property
        @cache
        def request_by_id(self):
            return createIdLoader(asyncSessionMaker, RequestModel)

        @property
        @cache
        def requests_by_createdby(self):
            return createFkeyLoader(asyncSessionMaker, RequestModel, foreignKeyName="createdby")

        @property
        @cache
        def form_by_id(self):
            return createIdLoader(asyncSessionMaker, FormModel)

        @property
        @cache
        def formtype_by_id(self):
            return createIdLoader(asyncSessionMaker, FormTypeModel)

        @property
        @cache
        def formcategory_by_id(self):
            return createIdLoader(asyncSessionMaker, FormCategoryModel)

        @property
        @cache
        def history_by_id(self):
            return createIdLoader(asyncSessionMaker, HistoryModel)

        @property
        @cache
        def histories_by_request_id(self):
            return createFkeyLoader(asyncSessionMaker, HistoryModel, foreignKeyName="request_id")

        @property
        @cache
        def section_by_id(self):
            return createIdLoader(asyncSessionMaker, SectionModel)

        @property
        @cache
        def section_by_form_id(self):
            return createFkeyLoader(asyncSessionMaker, SectionModel, foreignKeyName="form_id")

        @property
        @cache
        def part_by_id(self):
            return createIdLoader(asyncSessionMaker, PartModel)

        @property
        @cache
        def parts_by_section_id(self):
            return createFkeyLoader(asyncSessionMaker, PartModel, foreignKeyName="section_id")

        @property
        @cache
        def item_by_id(self):
            return createIdLoader(asyncSessionMaker, ItemModel)

        @property
        @cache
        def item_type_by_id(self):
            return createIdLoader(asyncSessionMaker, ItemTypeModel)

        @property
        @cache
        def item_category_by_id(self):
            return createIdLoader(asyncSessionMaker, ItemCategoryModel)

        @property
        @cache
        def items_by_part_id(self):
            return createFkeyLoader(asyncSessionMaker, ItemModel, foreignKeyName="part_id")

        # @property
        # @cache
        # def facilities_by_master_id(self):
        #     return createFkeyLoader(asyncSessionMaker, FacilityModel, foreignKeyName="master_facility_id")
    return Loaders()
