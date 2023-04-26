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


# def AsyncSessionFromInfo(info):
#     print(
#         "obsolte function used AsyncSessionFromInfo, use withInfo context manager instead"
#     )
#     return info.context["session"]

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
    async def resolve_reference(cls, id: strawberryA.ID):
        return UserGQLModel(id=id)


import datetime

# define the type help to get attribute name and name
@strawberryA.federation.type(
    keys=["id"], description="""Entity representing a request (digital form of a paper, aka "student request to the dean")"""
)
class RequestGQLModel:
    """
    Type representing a request in the system.
    This class extends the base `RequestModel` from the database and adds additional fields and methods needed for use in GraphQL.
    """
    @classmethod
    async def resolve_reference(cls, info: strawberryA.types.Info, id: strawberryA.ID):
        loader = getLoaders(info).requests
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
        loader = getLoaders(info).histories
        result = await loader.filter_by(form_id=self.id)
        return result


@strawberryA.federation.type(
    keys=["id"], description="""Entity representing a request history item"""
)
class HistoryGQLModel:
    """
    Type representing a request in the system.
    This class extends the base `RequestModel` from the database and adds additional fields and methods needed for use in GraphQL.
    """
    @classmethod
    async def resolve_reference(cls, info: strawberryA.types.Info, id: strawberryA.ID):
        loader = getLoaders(info).histories
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
        loader = getLoaders(info).formcategories
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
        loader = getLoaders(info).formtypes
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
    keys=["id"], description="""Entity representing a form, form is digitalized A4 sheet"""
)
class FormGQLModel:
    """
    Type representing a request in the system.
    This class extends the base `RequestModel` from the database and adds additional fields and methods needed for use in GraphQL.
    """
    @classmethod
    async def resolve_reference(cls, info: strawberryA.types.Info, id: strawberryA.ID):
        loader = getLoaders(info).forms
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

    @strawberryA.field(description="""Request's validity""")
    def valid(self) -> bool:
        return self.valid

    @strawberryA.field(description="""Request's status""")
    def status(self) -> bool:
        return self.status

    @strawberryA.field(description="Retrieves the sections related to this form (form has several sections)")
    async def sections(
        self, info: strawberryA.types.Info
    ) -> typing.List["SectionGQLModel"]:
        loader = getLoaders(info).sections
        sections = await loader.load(self.id)
        return sections

    @strawberryA.field(description="Retrieves the user who has initiated this request")
    async def creator(self, info: strawberryA.types.Info) -> "UserGQLModel":
        #user = UserGQLModel(id=self.createdby)
        return await UserGQLModel.resolve_reference(id=self.createdby)

    @strawberryA.field(description="Retrieves the type of form")
    async def type(self, info: strawberryA.types.Info) -> Union["FormTypeGQLModel", None]:
        result = await FormTypeGQLModel.resolve_reference(info, id=self.type_id)
        return result

    @strawberryA.field(description="Retrieves the editor")
    async def editor(self, info: strawberryA.types.Info) -> Union["FormEditorGQLModel", None]:
        result = await FormEditorGQLModel.resolve_reference(info, id=self.id)
        return result

from gql_forms.GraphResolvers import resolveUpdateForm
from typing import Optional

@strawberryA.input
class _FormUpdateGQLModel:
    lastchange: datetime.datetime
    name: Optional[str] = None
    name_en: Optional[str] = None
    valid: Optional[bool] = None

@strawberryA.federation.type(
    keys=["id"], description="""Entity representing a form editor"""
)
class FormEditorGQLModel:
    """
    """

    id: strawberryA.ID = None
    result: str = None

    @classmethod
    async def resolve_reference(cls, info: strawberryA.types.Info, id: strawberryA.ID):
        loader = getLoaders(info).forms
        result = await loader.load(id)
        if result is not None:
            result._type_definition = cls._type_definition  # little hack :)
        return result
    
    @strawberryA.field(
        description="""Description of operation (form update) result. "ok", if all went good."""
    )
    def result(self) -> str:
        return self.result
    
    @strawberryA.field(
        description="""Updates a form."""
    )
    async def update(self, info: strawberryA.types.Info, form: "FormUpdateGQLModel") -> "FormEditorGQLModel":
        async with withInfo(info) as session:
            lastchange = form.lastchange
            # print(lastchange)
            # updated = await resolveUpdateGroup(session,  id=self.id, data=group)
            # loader = getLoaders(info).groups
            updated = await resolveUpdateForm(session, id=self.id, data=form)
            #updated = await loader.update(self, extraValues=data)
            # print(updated)
            # print(group.lastchange)
            # print(updated.lastchange)
            if lastchange == form.lastchange:
                resultMsg = "fail"
            else:
                resultMsg = "ok"
            result = FormEditorGQLModel()
            result.id = self.id
            result.result = resultMsg
            return result


@strawberryA.federation.type(
    keys=["id"], description="""Type representing a section in the form"""
)
class SectionGQLModel:
    @classmethod
    async def resolve_reference(cls, info: strawberryA.types.Info, id: strawberryA.ID):
        loader = getLoaders(info).sections
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
        loader = getLoaders(info).parts
        result = await loader.load(section_id=self.id)
        return result

    @strawberryA.field(description="Retrieves the form owning this section")
    async def form(self, info: strawberryA.types.Info) -> "FormGQLModel":
        result = await FormGQLModel.resolve_reference(info, self.form_id)
        return result

    @strawberryA.field(description="Retrieves the editor")
    async def editor(self, info: strawberryA.types.Info) -> Union["SectionEditorGQLModel", None]:
        result = await SectionEditorGQLModel.resolve_reference(info, id=self.id)
        return result

@strawberryA.input
class SectionUpdateGQLModel:
    lastchange: datetime.datetime
    name: Optional[str] = None
    order: Optional[int] = None
    valid: Optional[bool] = None

from gql_forms.GraphResolvers import resolverUpdateSection

@strawberryA.federation.type(
    keys=["id"], description="""Entity representing a section editor"""
)
class SectionEditorGQLModel:
    """
    """

    id: strawberryA.ID = None
    result: str = None

    @classmethod
    async def resolve_reference(cls, info: strawberryA.types.Info, id: strawberryA.ID):
        loader = getLoaders(info).sections
        result = await loader.load(id)
        if result is not None:
            result._type_definition = cls._type_definition  # little hack :)
        return result
    
    @strawberryA.field(
        description="""Description of operation (form update) result. "ok", if all went good."""
    )
    def result(self) -> str:
        return self.result
    
    @strawberryA.field(
        description="""Updates a section."""
    )
    async def update(self, info: strawberryA.types.Info, section: SectionUpdateGQLModel) -> "SectionEditorGQLModel":
        async with withInfo(info) as session:
            lastchange = section.lastchange
            # print(lastchange)
            # updated = await resolveUpdateGroup(session,  id=self.id, data=group)
            # loader = getLoaders(info).groups
            updated = await resolverUpdateSection(session, id=self.id, data=section)
            #updated = await loader.update(self, extraValues=data)
            # print(updated)
            # print(group.lastchange)
            # print(updated.lastchange)
            if lastchange == section.lastchange:
                resultMsg = "fail"
            else:
                resultMsg = "ok"
            result = SectionEditorGQLModel()
            result.id = self.id
            result.result = resultMsg
            return result
        
    @strawberryA.field(
        description="""Inserts a part."""
    )
    async def insert_part(self, info: strawberryA.types.Info, part: "PartUpdateGQLModel") -> "PartGQLModel":
        async with withInfo(info) as session:
            result = await resolveInsertPart(session, part)
        return await PartGQLModel.resolve_reference(info, result.id)
            
    # @strawberryA.field(
    #     description="""Updates a part."""
    # )
    # async def update_part(self, info: strawberryA.types.Info, part: "PartUpdateGQLModel") -> "PartGQLModel":
    #     async with withInfo(info) as session:
    #         result = await resolveUpdatePart(session, part)
    #     return PartGQLModel.resolve_reference(info, result.id)
            

@strawberryA.input
class PartUpdateGQLModel:
    lastchange: datetime.datetime
    name: Optional[str] = None
    order: Optional[int] = None

@strawberryA.federation.type(
    keys=["id"], description="""Type representing a part in the section"""
)
class PartGQLModel:
    @classmethod
    async def resolve_reference(cls, info: strawberryA.types.Info, id: strawberryA.ID):
        loader = getLoaders(info).parts
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

    @strawberryA.field(description="Retrieves the section owning this part")
    async def section(self, info: strawberryA.types.Info) -> "SectionGQLModel":
        result = await SectionGQLModel.resolve_reference(info, self.section_id)
        return result

    @strawberryA.field(description="Retrieves the items related to this part")
    async def items(self, info: strawberryA.types.Info) -> typing.List["ItemGQLModel"]:
        loader = getLoaders(info).items
        result = await loader.filer_by(part_id=self.id)
        return result

    @strawberryA.field(description="Retrieves the editor")
    async def editor(self, info: strawberryA.types.Info) -> Union["PartEditorGQLModel", None]:
        result = await PartEditorGQLModel.resolve_reference(info, id=self.id)
        return result

from gql_forms.GraphResolvers import resolverUpdatePart
@strawberryA.federation.type(
    keys=["id"], description="""Entity representing a part editor"""
)
class PartEditorGQLModel:
    """
    """

    id: strawberryA.ID = None
    result: str = None

    @classmethod
    async def resolve_reference(cls, info: strawberryA.types.Info, id: strawberryA.ID):
        loader = getLoaders(info).parts
        result = await loader.load(id)
        if result is not None:
            result._type_definition = cls._type_definition  # little hack :)
        return result
    
    @strawberryA.field(
        description="""Description of operation (form update) result. "ok", if all went good."""
    )
    def result(self) -> str:
        return self.result
    
    @strawberryA.field(
        description="""Updates a section."""
    )
    async def update(self, info: strawberryA.types.Info, part: PartUpdateGQLModel) -> "PartEditorGQLModel":
        async with withInfo(info) as session:
            lastchange = part.lastchange
            # print(lastchange)
            # updated = await resolveUpdateGroup(session,  id=self.id, data=group)
            # loader = getLoaders(info).groups
            updated = await resolverUpdatePart(session, id=self.id, data=part)
            #updated = await loader.update(self, extraValues=data)
            # print(updated)
            # print(group.lastchange)
            # print(updated.lastchange)
            if lastchange == part.lastchange:
                resultMsg = "fail"
            else:
                resultMsg = "ok"
            result = PartEditorGQLModel()
            result.id = self.id
            result.result = resultMsg
            return result
        
    @strawberryA.field(
        description="""Inserts an item."""
    )
    async def insert_item(self, info: strawberryA.types.Info, item: "ItemUpdateGQLModel") -> "ItemGQLModel":
        async with withInfo(info) as session:
            result = await resolveInsertItem(session, item)
        return await ItemGQLModel.resolve_reference(info, result.id)

@strawberryA.input
class ItemUpdateGQLModel:
    lastchange: datetime.datetime
    name: Optional[str] = None
    order: Optional[int] = None
    value: Optional[str] = None
    type_id: Optional[strawberryA.ID] = None

@strawberryA.federation.type(
    keys=["id"], description="""Type representing an item in the form"""
)
class ItemGQLModel:
    @classmethod
    async def resolve_reference(cls, info: strawberryA.types.Info, id: strawberryA.ID):
        loader = getLoaders(info).items
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

    @strawberryA.field(description="""Item's order""")
    def order(self) -> str:
        return self.order

    @strawberryA.field(description="""Item's time of last update""")
    def lastchange(self) -> datetime.datetime:
        return self.lastchange

    @strawberryA.field(description="""Item's value """)
    def value(self) -> str:
        return self.value

    @strawberryA.field(description="Retrieves the part owning the item")
    async def part(self, info: strawberryA.types.Info) -> "PartGQLModel":
        result = await PartGQLModel.resolve_reference(info, self.part_id)
        return result

    @strawberryA.field(description="Retrieves the item type")
    async def type(self, info: strawberryA.types.Info) -> "ItemTypeGQLModel":
        result = await ItemTypeGQLModel.resolve_reference(info, self.type_id)
        return result

    @strawberryA.field(description="Retrieves the editor")
    async def editor(self, info: strawberryA.types.Info) -> Union["ItemEditorGQLModel", None]:
        result = await ItemEditorGQLModel.resolve_reference(info, id=self.id)
        return result

@strawberryA.federation.type(
    keys=["id"], description="""Entity representing an item editor"""
)
class ItemEditorGQLModel:
    """
    """

    id: strawberryA.ID = None
    result: str = None

    @classmethod
    async def resolve_reference(cls, info: strawberryA.types.Info, id: strawberryA.ID):
        loader = getLoaders(info).items
        result = await loader.load(id)
        if result is not None:
            result._type_definition = cls._type_definition  # little hack :)
        return result
    
    @strawberryA.field(
        description="""Description of operation (form update) result. "ok", if all went good."""
    )
    def result(self) -> str:
        return self.result
    
    @strawberryA.field(
        description="""Updates a section."""
    )
    async def update(self, info: strawberryA.types.Info, item: ItemUpdateGQLModel) -> "ItemEditorGQLModel":
        async with withInfo(info) as session:
            lastchange = item.lastchange
            # print(lastchange)
            # updated = await resolveUpdateGroup(session,  id=self.id, data=group)
            # loader = getLoaders(info).groups
            updated = await resolverUpdateItem(session, id=self.id, data=item)
            #updated = await loader.update(self, extraValues=data)
            # print(updated)
            # print(group.lastchange)
            # print(updated.lastchange)
            if lastchange == item.lastchange:
                resultMsg = "fail"
            else:
                resultMsg = "ok"
            result = ItemEditorGQLModel()
            result.id = self.id
            result.result = resultMsg
            return result


@strawberryA.federation.type(
    keys=["id"], description="""Type representing an item type"""
)
class ItemTypeGQLModel:
    @classmethod
    async def resolve_reference(cls, info: strawberryA.types.Info, id: strawberryA.ID):
        loader = getLoaders(info).itemtypes
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
        #result = await ItemCategoryGQLModel(info, self.category_id)
        return await ItemCategoryGQLModel(info, self.category_id)

@strawberryA.federation.type(
    keys=["id"], description="""Type representing an item category"""
)
class ItemCategoryGQLModel:
    @classmethod
    async def resolve_reference(cls, info: strawberryA.types.Info, id: strawberryA.ID):
        loader = getLoaders(info).itemcategories
        result = await loader.load(id)
        if result is not None:
            result._type_definition = cls._type_definition  # little hack :)
        return result

    @strawberryA.field(description="""Entity primary key""")
    def id(self) -> strawberryA.ID:
        return self.id

    @strawberryA.field(description="""Category name""")
    def name(self) -> str:
        return self.name


###########################################################################################################################
#
# zde definujte svuj Query model
#
###########################################################################################################################
from gql_forms.GraphResolvers import resolveRequestByUser
from gql_forms.GraphResolvers import requestselect, formtypeselect, formcategorySelect
from gql_forms.GraphResolvers import itemtypeselect, itemcategoryselect, createNewRequest


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
        loader = getLoaders(info).requests
        result = await loader.execute_select(requestselect.offset(skip).limit(limit))
        return result

    @strawberryA.field(description="""Finds an request by their id""")
    async def requests_by_creator(
        self, info: strawberryA.types.Info, id: strawberryA.ID
    ) -> List[RequestGQLModel]:
        loader = getLoaders(info).requests
        result = await loader.filter_by(createdby=id)
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
        loader = getLoaders(info).formcategories
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
        loader = getLoaders(info).formtypes
        stmt = formtypeselect.offset(skip).limit(limit)
        result = await loader.execute_select(stmt)
        return result

    @strawberryA.field(description="Retrieves the item categories")
    async def item_category_page(
        self, info: strawberryA.types.Info, skip: int = 0, limit: int = 10
    ) -> List[ItemCategoryGQLModel]:
        loader = getLoaders(info).itemcategories
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
        loader = getLoaders(info).itemtypes
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


    @strawberryA.field(description="Creates an empty request")
    async def new_request(
        self, info: strawberryA.types.Info, formtype_id: strawberryA.ID
    ) -> Union[RequestGQLModel, None]:
        async with withInfo(info) as session:
            result = await createNewRequest(session=session, formtypeid=formtype_id)
        return await RequestGQLModel.resolve_reference(info, result.id)


###########################################################################################################################
#
#
# Mutations
#
#
###########################################################################################################################

from typing import Optional
import datetime

@strawberryA.input
class FormInsertGQLModel:
    name: str
    
    id: Optional[strawberryA.ID] = None
    form_type_id: Optional[strawberryA.ID] = None
    place: Optional[str] = ""
    published_date: Optional[datetime.datetime] = datetime.datetime.now()
    reference: Optional[str] = ""
    valid: Optional[bool] = True

@strawberryA.input
class FormUpdateGQLModel:
    lastchange: datetime.datetime
    id: strawberryA.ID

    name: Optional[str] = None
    form_type_id: Optional[strawberryA.ID] = None
    place: Optional[str] = None
    published_date: Optional[datetime.datetime] = None
    reference: Optional[str] = None
    valid: Optional[bool] = None
    
    
@strawberryA.type
class FormResultGQLModel:
    id: strawberryA.ID = None
    msg: str = None

    @strawberryA.field(description="""Result of form operation""")
    async def form(self, info: strawberryA.types.Info) -> Union[FormGQLModel, None]:
        result = await FormGQLModel.resolve_reference(info, self.id)
        return result
   
@strawberryA.federation.type(extend=True)
class Mutation:
    @strawberryA.mutation
    async def form_insert(self, info: strawberryA.types.Info, form: FormInsertGQLModel) -> FormResultGQLModel:
        loader = getLoaders(info).forms
        row = await loader.insert(form)
        result = FormResultGQLModel()
        result.msg = "ok"
        result.id = row.id
        return result

    @strawberryA.mutation
    async def form_update(self, info: strawberryA.types.Info, form: FormUpdateGQLModel) -> FormResultGQLModel:
        loader = getLoaders(info).forms
        row = await loader.update(form)
        result = FormResultGQLModel()
        result.msg = "ok"
        result.id = form.id
        if row is None:
            result.msg = "fail"
            
        return result


###########################################################################################################################
#
# Schema je pouzito v main.py, vsimnete si parametru types, obsahuje vyjmenovane modely. Bez explicitniho vyjmenovani
# se ve schema objevi jen ty struktury, ktere si strawberry dokaze odvodit z Query. Protoze v teto konkretni implementaci
# nektere modely nejsou s Query propojene je potreba je explicitne vyjmenovat. Jinak ve federativnim schematu nebude
# dostupne rozsireni, ktere tento prvek federace implementuje.
#
###########################################################################################################################

schema = strawberryA.federation.Schema(Query, types=(UserGQLModel,), mutation=Mutation)
