@strawberryA.federation.type(keys = ["id"] ,description="""Type representing a section in the workflow""")
class SectionGQLModel:
   
     @strawberryA.field(description="""Finds an section by their id""")
     async def id(self, info: strawberryA.types.Info) -> Union[str, None]:
         result = self.id
         #resovle will be ask
         return result

     @strawberryA.field(description="""Finds an section by their id""")
     async def name(self, info: strawberryA.types.Info) -> Union[str, None]:
         result = self.name
         #resovle will be ask
         return result

     @strawberryA.field(description="Retrieves the parts related to this section")
     async def parts(self, info: strawberryA.types.Info) -> List[PartGQLModel]:
        session = AsyncSessionFromInfo(info)
        parts = await resolvePartsForSection(session, self.id)
        return parts

     @strawberryA.field(description="Updates the name of the section")
     async def update(self, info: strawberryA.types.Info, name: Optional[str] = None) -> SectionGQLModel:
        session = AsyncSessionFromInfo(info)
        update_data = {}
        if name is not None:
            update_data["name"] = name
        updated_section = await resolverUpdateSection(session, self.id, update_data)
        return updated_section

