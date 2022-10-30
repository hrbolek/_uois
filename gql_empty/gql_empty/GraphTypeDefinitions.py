from typing import List, Union
import typing
from unittest import result
import strawberry as strawberryA
import uuid

def AsyncSessionFromInfo(info):
    return info.context['session']

###########################################################################################################################
#
# zde definujte sve GQL modely
# - nove, kde mate zodpovednost
# - rozsirene, ktere existuji nekde jinde a vy jim pridavate dalsi atributy
#
###########################################################################################################################

    

###########################################################################################################################
#
# zde definujte svuj Query model
#
###########################################################################################################################

@strawberryA.type(description="""Type for query root""")
class Query:
   
    @strawberryA.field(description="""Finds an workflow by their id""")
    async def say_hello(self, info: strawberryA.types.Info, id: uuid.UUID) -> Union[str, None]:
        result = f'Hello {id}'
        return result
