from typing import List, Union
import typing
import strawberry as strawberryA
import uuid
from contextlib import asynccontextmanager


@asynccontextmanager
async def withInfo(info):
    asyncSessionMaker = info.context["asyncSessionMaker"]
    async with asyncSessionMaker() as session:
        try:
            yield session
        finally:
            pass


def AsyncSessionFromInfo(info):
    print(
        "obsolte function used AsyncSessionFromInfo, use withInfo context manager instead"
    )
    return info.context["session"]

def getLoaders(info):
    return info.context['all']

###########################################################################################################################
#
# zde definujte sve GQL modely
# - nove, kde mate zodpovednost
# - rozsirene, ktere existuji nekde jinde a vy jim pridavate dalsi atributy
#
###########################################################################################################################
from gql_forms.GraphResolvers import (
    resolveRequestById,
    resolveRequestAll,
    resolveSectionsForRequest,
    resolverUpdateRequest,
    resolveInsertRequest,
    resolveRequestsByThreeLetters,
)

# from gql_forms.GraphResolvers import resolveRequestsByThreeLetters
from gql_forms.GraphResolvers import (
    resolveSectionById,
    resolveSectionAll,
    resolvePartsForSection,
    resolverUpdateSection,
    resolveInsertSection,
)
from gql_forms.GraphResolvers import (
    resolvePartById,
    resolvePartAll,
    resolveItemsForPart,
    resolverUpdatePart,
    resolveInsertPart,
)
from gql_forms.GraphResolvers import (
    resolveItemById,
    resolveItemAll,
    resolverUpdateItem,
    resolveInsertItem,
)

@strawberryA.federation.type(extend=True, keys=["id"])
class UserGQLModel:

    id: strawberryA.ID = strawberryA.federation.field(external=True)

    @classmethod
    def resolve_reference(cls, id: strawberryA.ID):
        return UserGQLModel(id=id)


import datetime

# define the type help to get attribute name and name
@strawberryA.federation.type(
    keys=["id"], description="""Entity representing a request"""
)
class RequestGQLModel:
    """
    Type representing a request in the system.
    This class extends the base `RequestModel` from the database and adds additional fields and methods needed for use in GraphQL.
    """
    @classmethod
    async def resolve_reference(cls, info: strawberryA.types.Info, id: strawberryA.ID):
        loader = getLoaders(info).request_by_id
        result = await loader.load(id)
        if result is not None:
            result._type_definition = cls._type_definition  # little hack :)
        return result

    @strawberryA.field(description="""Entity primary key""")
    def id(self) -> strawberryA.ID:
        return self.id

    @strawberryA.field(description="""Request's name (like Vacation)""")
    def name(self) -> str:
        return self.name

    @strawberryA.field(description="""Request's time of last update""")
    def lastchange(self) -> datetime.datetime:
        return self.lastchange

    @strawberryA.field(description="""Request's time of last update""")
    def creator(self) -> UserGQLModel:
        return UserGQLModel(id=self.createdby)

    @strawberryA.field(description="""Request's time of last update""")
    async def histories(self, info: strawberryA.types.Info) -> List["HistoryGQLModel"]:
        loader = getLoaders(info).histories_by_request_id
        result = await loader.load(self.id)
        return result


@strawberryA.federation.type(
    keys=["id"], description="""Entity representing a request"""
)
class HistoryGQLModel:
    """
    Type representing a request in the system.
    This class extends the base `RequestModel` from the database and adds additional fields and methods needed for use in GraphQL.
    """
    @classmethod
    async def resolve_reference(cls, info: strawberryA.types.Info, id: strawberryA.ID):
        loader = getLoaders(info).history_by_id
        result = await loader.load(id)
        if result is not None:
            result._type_definition = cls._type_definition  # little hack :)
        return result

    @strawberryA.field(description="""Entity primary key""")
    def id(self) -> strawberryA.ID:
        return self.id

    @strawberryA.field(description="""History comment""")
    def name(self) -> str:
        return self.name

    @strawberryA.field(description="""Time of last update""")
    def lastchange(self) -> datetime.datetime:
        return self.lastchange

    @strawberryA.field(description="""Request which history belongs to""")
    async def request(self, info: strawberryA.types.Info) -> "RequestGQLModel":
        result = await RequestGQLModel.resolve_reference(info, self.request_id)
        return result

    @strawberryA.field(description="""History form""")
    async def form(self, info: strawberryA.types.Info) -> "FormGQLModel":
        result = await FormGQLModel.resolve_reference(info, self.form_id)
        return result

@strawberryA.federation.type(
    keys=["id"], description="""Entity representing a category of form types"""
)
class FormCategoryGQLModel:
    """
    """
    @classmethod
    async def resolve_reference(cls, info: strawberryA.types.Info, id: strawberryA.ID):
        loader = getLoaders(info).formcategory_by_id
        result = await loader.load(id)
        if result is not None:
            result._type_definition = cls._type_definition  # little hack :)
        return result

    @strawberryA.field(description="""Entity primary key""")
    def id(self) -> strawberryA.ID:
        return self.id

    @strawberryA.field(description="""Name """)
    def name(self) -> str:
        return self.name

    @strawberryA.field(description="""Name """)
    def name_en(self) -> str:
        return self.name_en

    @strawberryA.field(description="""Time of last update""")
    def lastchange(self) -> datetime.datetime:
        return self.lastchange


@strawberryA.federation.type(
    keys=["id"], description="""Entity representing a category of form types"""
)
class FormTypeGQLModel:
    """
    """
    @classmethod
    async def resolve_reference(cls, info: strawberryA.types.Info, id: strawberryA.ID):
        loader = getLoaders(info).formtype_by_id
        result = await loader.load(id)
        if result is not None:
            result._type_definition = cls._type_definition  # little hack :)
        return result

    @strawberryA.field(description="""Entity primary key""")
    def id(self) -> strawberryA.ID:
        return self.id

    @strawberryA.field(description="""Request's name (like Vacation)""")
    def name(self) -> str:
        return self.name

    @strawberryA.field(description="""Request's name (like Vacation)""")
    def name_en(self) -> str:
        return self.name_en

    @strawberryA.field(description="""Request's time of last update""")
    def lastchange(self) -> datetime.datetime:
        return self.lastchange

    @strawberryA.field(description="""Request's time of last update""")
    async def category(self, info: strawberryA.types.Info) -> "FormCategoryGQLModel":
        result = await FormCategoryGQLModel.resolve_reference(info, self.category_id)
        return result

@strawberryA.federation.type(
    keys=["id"], description="""Entity representing a form"""
)
class FormGQLModel:
    """
    Type representing a request in the system.
    This class extends the base `RequestModel` from the database and adds additional fields and methods needed for use in GraphQL.
    """
    @classmethod
    async def resolve_reference(cls, info: strawberryA.types.Info, id: strawberryA.ID):
        loader = getLoaders(info).form_by_id
        result = await loader.load(id)
        if result is not None:
            result._type_definition = cls._type_definition  # little hack :)
        return result

    @strawberryA.field(description="""Entity primary key""")
    def id(self) -> strawberryA.ID:
        return self.id

    @strawberryA.field(description="""Request's name (like Vacation)""")
    def name(self) -> str:
        return self.name

    @strawberryA.field(description="""Request's name (like Vacation)""")
    def name_en(self) -> str:
        return self.name_en

    @strawberryA.field(description="""Request's time of last update""")
    def lastchange(self) -> datetime.datetime:
        return self.lastchange

    @strawberryA.field(description="""Request's valid status""")
    def valid(self) -> bool:
        return self.valid

    @strawberryA.field(description="""Request's valid status""")
    def status(self) -> bool:
        return self.status

    @strawberryA.field(description="Retrieves the sections related to this request")
    async def sections(
        self, info: strawberryA.types.Info
    ) -> typing.List["SectionGQLModel"]:
        loader = getLoaders(info).section_by_form_id
        sections = await loader.load(self.id)
        return sections

    @strawberryA.field(description="Retrieves the user who has initiated this request")
    async def creator(self, info: strawberryA.types.Info) -> "UserGQLModel":
        user = UserGQLModel(id=self.createdby)
        return user

    @strawberryA.field(description="Retrieves the type of form")
    async def type(self, info: strawberryA.types.Info) -> Union["FormTypeGQLModel", None]:
        result = await FormTypeGQLModel.resolve_reference(info, id=self.type_id)
        return result



@strawberryA.federation.type(
    keys=["id"], description="""Type representing a section in the workflow"""
)
class SectionGQLModel:
    @classmethod
    async def resolve_reference(cls, info: strawberryA.types.Info, id: strawberryA.ID):
        loader = getLoaders(info).section_by_id
        result = await loader.load(id)
        if result is not None:
            result._type_definition = cls._type_definition  # little hack :)
        return result

    @strawberryA.field(description="""Entity primary key""")
    def id(self) -> strawberryA.ID:
        return self.id

    @strawberryA.field(description="""Section's name""")
    def name(self) -> str:
        return self.name

    @strawberryA.field(description="""Section's time of last update""")
    def lastchange(self) -> datetime.datetime:
        return self.lastchange

    @strawberryA.field(description="""Section's order""")
    def order(self) -> int:
        return self.order

    @strawberryA.field(description="Retrieves the parts related to this section")
    async def parts(self, info: strawberryA.types.Info) -> typing.List["PartGQLModel"]:
        loader = getLoaders(info).parts_by_section_id
        result = await loader.load(self.id)
        return result

    @strawberryA.field(description="Retrieves the parts related to this section")
    async def form(self, info: strawberryA.types.Info) -> "FormGQLModel":
        result = await FormGQLModel.resolve_reference(info, self.form_id)
        return result

@strawberryA.federation.type(
    keys=["id"], description="""Type representing a part in the workflow"""
)
class PartGQLModel:
    @classmethod
    async def resolve_reference(cls, info: strawberryA.types.Info, id: strawberryA.ID):
        loader = getLoaders(info).part_by_id
        result = await loader.load(id)
        if result is not None:
            result._type_definition = cls._type_definition  # little hack :)
        return result

    @strawberryA.field(description="""Entity primary key""")
    def id(self) -> strawberryA.ID:
        return self.id

    @strawberryA.field(description="""Part's name (part for Student)""")
    def name(self) -> str:
        return self.name

    @strawberryA.field(description="""Part's time of last update""")
    def lastchange(self) -> datetime.datetime:
        return self.lastchange

    @strawberryA.field(description="""Part's order""")
    def order(self) -> int:
        return self.order

    @strawberryA.field(description="Retrieves the items related to this part")
    async def section(self, info: strawberryA.types.Info) -> "SectionGQLModel":
        result = await SectionGQLModel.resolve_reference(info, self.section_id)
        return result

    @strawberryA.field(description="Retrieves the items related to this part")
    async def items(self, info: strawberryA.types.Info) -> typing.List["ItemGQLModel"]:
        loader = getLoaders(info).items_by_part_id
        result = await loader.load(self.id)
        return result

@strawberryA.federation.type(
    keys=["id"], description="""Type representing an item in the workflow"""
)
class ItemGQLModel:
    @classmethod
    async def resolve_reference(cls, info: strawberryA.types.Info, id: strawberryA.ID):
        loader = getLoaders(info).item_by_id
        result = await loader.load(id)
        if result is not None:
            result._type_definition = cls._type_definition  # little hack :)
        return result

    @strawberryA.field(description="""Entity primary key""")
    def id(self) -> strawberryA.ID:
        return self.id

    @strawberryA.field(description="""Item's name (like Name)""")
    def name(self) -> str:
        return self.name

    @strawberryA.field(description="""Item's name (like Name)""")
    def order(self) -> str:
        return self.order

    @strawberryA.field(description="""Item's time of last update""")
    def lastchange(self) -> datetime.datetime:
        return self.lastchange

    @strawberryA.field(description="""Item's name (like Name)""")
    def value(self) -> str:
        return self.value

    @strawberryA.field(description="Retrieves the items related to this part")
    async def part(self, info: strawberryA.types.Info) -> "PartGQLModel":
        result = await PartGQLModel.resolve_reference(info, self.part_id)
        return result

    @strawberryA.field(description="Retrieves the items related to this part")
    async def type(self, info: strawberryA.types.Info) -> "ItemTypeGQLModel":
        result = await ItemTypeGQLModel.resolve_reference(info, self.type_id)
        return result

@strawberryA.federation.type(
    keys=["id"], description="""Type representing an item in the workflow"""
)
class ItemTypeGQLModel:
    @classmethod
    async def resolve_reference(cls, info: strawberryA.types.Info, id: strawberryA.ID):
        loader = getLoaders(info).item_type_by_id
        result = await loader.load(id)
        if result is not None:
            result._type_definition = cls._type_definition  # little hack :)
        return result

    @strawberryA.field(description="""Entity primary key""")
    def id(self) -> strawberryA.ID:
        return self.id

    @strawberryA.field(description="""Type name""")
    def name(self) -> str:
        return self.name

    @strawberryA.field(description="""Type category""")
    async def category(self, info: strawberryA.types.Info) -> "ItemCategoryGQLModel":
        result = await ItemCategoryGQLModel(info, self.category_id)
        return result

@strawberryA.federation.type(
    keys=["id"], description="""Type representing an item in the workflow"""
)
class ItemCategoryGQLModel:
    @classmethod
    async def resolve_reference(cls, info: strawberryA.types.Info, id: strawberryA.ID):
        loader = getLoaders(info).item_category_by_id
        result = await loader.load(id)
        if result is not None:
            result._type_definition = cls._type_definition  # little hack :)
        return result

    @strawberryA.field(description="""Entity primary key""")
    def id(self) -> strawberryA.ID:
        return self.id

    @strawberryA.field(description="""Item's name (like Name)""")
    def name(self) -> str:
        return self.name



###########################################################################################################################
#
# zde definujte svuj Query model
#
###########################################################################################################################
from gql_forms.GraphResolvers import resolveRequestByUser
from gql_forms.GraphResolvers import requestselect, formtypeselect, formcategorySelect
from gql_forms.GraphResolvers import itemtypeselect, itemcategoryselect


@strawberryA.type(description="""Type for query root""")
class Query:
    @strawberryA.field(description="""Say hello to the world""")
    async def say_hello_forms(
        self, info: strawberryA.types.Info, id: strawberryA.ID
    ) -> Union[str, None]:
        result = f"Hello {id}"
        return result

    @strawberryA.field(description="""Finds an request by their id""")
    async def request_by_id(
        self, info: strawberryA.types.Info, id: strawberryA.ID
    ) -> Union[RequestGQLModel, None]:
        result = await RequestGQLModel.resolve_reference(info, id)
        return result

    @strawberryA.field(description="Retrieves all requests")
    async def requests_page(
        self, info: strawberryA.types.Info, skip: int=0, limit: int=10
    ) -> List[RequestGQLModel]:
        loader = getLoaders(info).request_by_id
        result = await loader.execute_select(requestselect.offset(skip).limit(limit))
        return result

    @strawberryA.field(description="""Finds an request by their id""")
    async def requests_by_creator(
        self, info: strawberryA.types.Info, id: strawberryA.ID
    ) -> List[RequestGQLModel]:
        loader = getLoaders(info).requests_by_createdby
        result = await loader.load(id)
        return result

    @strawberryA.field(description="Retrieves requests by three letters in their name")
    async def requests_by_letters(
        self, info: strawberryA.types.Info, letters: str
    ) -> List[RequestGQLModel]:
        async with withInfo(info) as session:
            requests = await resolveRequestsByThreeLetters(session, letters=letters)
            return requests

    @strawberryA.field(description="Retrieves the form category")
    async def form_category_by_id(
        self, info: strawberryA.types.Info, id: strawberryA.ID
    ) -> Union[FormCategoryGQLModel, None]:
        result = await FormCategoryGQLModel.resolve_reference(info=info, id=id)
        return result

    @strawberryA.field(description="Retrieves the form category")
    async def form_category_page(
        self, info: strawberryA.types.Info, skip: int = 0, limit: int = 10
    ) -> List[FormCategoryGQLModel]:
        loader = getLoaders(info).formcategory_by_id
        stmt = formcategorySelect.offset(skip).limit(limit)
        result = await loader.execute_select(stmt)
        return result

    @strawberryA.field(description="Retrieves the form type")
    async def form_type_by_id(
        self, info: strawberryA.types.Info, id: strawberryA.ID
    ) -> Union[FormTypeGQLModel, None]:
        result = await FormTypeGQLModel.resolve_reference(info=info, id=id)
        return result

    @strawberryA.field(description="Retrieves the form type")
    async def form_type_page(
        self, info: strawberryA.types.Info, skip: int = 0, limit: int = 10
    ) -> List[FormTypeGQLModel]:
        loader = getLoaders(info).formtype_by_id
        stmt = formtypeselect.offset(skip).limit(limit)
        result = await loader.execute_select(stmt)
        return result

    @strawberryA.field(description="Retrieves the item categories")
    async def item_category_page(
        self, info: strawberryA.types.Info, skip: int = 0, limit: int = 10
    ) -> List[ItemCategoryGQLModel]:
        loader = getLoaders(info).item_category_by_id
        stmt = itemcategoryselect.offset(skip).limit(limit)
        result = await loader.execute_select(stmt)
        return result

    @strawberryA.field(description="Retrieves the item category")
    async def item_category_by_id(
        self, info: strawberryA.types.Info, id: strawberryA.ID
    ) -> Union[ItemCategoryGQLModel, None]:
        result = await ItemCategoryGQLModel.resolve_reference(info=info, id=id)
        return result

    @strawberryA.field(description="Retrieves the item types")
    async def item_type_page(
        self, info: strawberryA.types.Info, skip: int = 0, limit: int = 10
    ) -> List[ItemCategoryGQLModel]:
        loader = getLoaders(info).item_type_by_id
        stmt = itemtypeselect.offset(skip).limit(limit)
        result = await loader.execute_select(stmt)
        return result


    @strawberryA.field(description="Retrieves the item type")
    async def item_type_by_id(
        self, info: strawberryA.types.Info, id: strawberryA.ID
    ) -> Union[ItemTypeGQLModel, None]:
        result = await ItemTypeGQLModel.resolve_reference(info=info, id=id)
        return result

    @strawberryA.field(description="Retrieves the item type")
    async def item_by_id(
        self, info: strawberryA.types.Info, id: strawberryA.ID
    ) -> Union[ItemGQLModel, None]:
        result = await ItemGQLModel.resolve_reference(info=info, id=id)
        return result


###########################################################################################################################
#
# Schema je pouzito v main.py, vsimnete si parametru types, obsahuje vyjmenovane modely. Bez explicitniho vyjmenovani
# se ve schema objevi jen ty struktury, ktere si strawberry dokaze odvodit z Query. Protoze v teto konkretni implementaci
# nektere modely nejsou s Query propojene je potreba je explicitne vyjmenovat. Jinak ve federativnim schematu nebude
# dostupne rozsireni, ktere tento prvek federace implementuje.
#
###########################################################################################################################

schema = strawberryA.federation.Schema(Query, types=(UserGQLModel,))
