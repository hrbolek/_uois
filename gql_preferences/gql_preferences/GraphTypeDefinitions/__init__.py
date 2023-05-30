import strawberry

from .query import Query
from .mutation import Mutation

schema = strawberry.federation.Schema(query=Query, mutation=Mutation)
# schema = strawberry.federation.Schema(query=Query)