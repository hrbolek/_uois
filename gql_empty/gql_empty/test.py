@strawberryA.federation.type(keys=["id"], description="Type representing a request in the system")
class RequestGQLModel:
    """
    Type representing a request in the system.
    This class extends the base `RequestModel` from the database and adds additional fields and methods needed for use in GraphQL.
    """
    
    id: strawberryA.ID = strawberryA.federation.field(external=True)
    name: str = strawberryA.Field(description="The name of the request")
    valid: bool = strawberryA.Field(description="Indicates whether the request is valid or not")

    @classmethod
    def resolve_reference(cls, id: strawberryA.ID):
        return RequestGQLModel(id=id)
    
    @strawberryA.field(description="Retrieves the sections related to this request")
    async def sections(self, info: strawberryA.types.Info) -> List[SectionGQLModel]:
        session = AsyncSessionFromInfo(info)
        sections = await resolveSectionsForRequest(session, self.id)
        return sections
    
    @strawberryA.field(description="Updates the name and valid status of the request")
    async def update(self, info: strawberryA.types.Info, name: Optional[str] = None, valid: Optional[bool] = None) -> RequestGQLModel:
        session = AsyncSessionFromInfo(info)
        update_data = {}
        if name is not None:
            update_data["name"] = name
        if valid is not None:
            update_data["valid"] = valid
        updated_request = await resolverUpdateRequest(session, self.id, update_data)
        return updated_request
