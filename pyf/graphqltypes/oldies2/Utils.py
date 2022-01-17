from graphene import Field, List, Mutation


def extractSession(info):
    #return info.context['request'].scope['db_session']
    assert not info.context is None, 'Got Bad Context'
    return info.context.get('session')

def attachResolverForRelation11(TypeA, TypeB, ItemNameA=None, ItemNameB=None, resolverA=None, resolverB=None):
    setattr(TypeA, ItemNameA, Field(TypeB, resolver=resolverA))
    setattr(TypeB, ItemNameB, Field(TypeA, resolver=resolverB))
    pass

def attachResolverForRelation1N(TypeA, TypeB, ItemNameA=None, ItemNameB=None, resolverA=None, resolverB=None):
    print(f'setting up for {TypeA}.{ItemNameA} Field(List(), resolver={resolverA}')
    setattr(TypeA, ItemNameA, Field(List(TypeB), resolver=resolverA))
    setattr(TypeB, ItemNameB, Field(TypeA, resolver=resolverB))
    pass

def attachResolverForRelationNM(TypeA, TypeB, ItemNameA=None, ItemNameB=None, resolverA=None, resolverB=None):
    setattr(TypeA, ItemNameA, Field(List(TypeB), resolver=resolverA))
    setattr(TypeB, ItemNameB, Field(List(TypeA), resolver=resolverB))
    pass

def createResolverById(MastersDBModel, MastersItemName):
    def resolver(parent, info):
        session = extractSession(info)
        masterDbRecord = session.query(MastersDBModel).get(parent.id)
        return getattr(masterDbRecord, MastersItemName, f'item {MastersItemName} not defined on {MastersDBModel}')
    return resolver

def createRootByName(MastersDBModel, MastersItemName):
    def resolver(parent, info):
        session = extractSession(info)
        masterDbRecord = session.query(MastersDBModel).filter(MastersDBModel.name == parent.name).first()
        return getattr(masterDbRecord, MastersItemName, f'item {MastersItemName} not defined on {MastersDBModel}')
    return resolver

def createRootResolverById(MastersDBModel):
    def resolver(parent, info, id):
        session = extractSession(info)
        masterDbRecord = session.query(MastersDBModel).get(id)
        return masterDbRecord
    return resolver

def createRootResolverByName(MastersDBModel):
    def resolver(parent, info, name):
        session = extractSession(info)
        masterDbRecord = session.query(MastersDBModel).filter(MastersDBModel.name == name).first()
        return masterDbRecord
    return resolver

from graphene import Mutation, Boolean
def createMutationClass(DbClassModel, MutationResultType, parentItemName=None, **arguments):
    """creates subclass if graphene.Mutation which creates DBRecord and returns appropriate graphene type

    Parameters
    ----------
    DbClassModel: SQLAlchemyModel
        Model of a database table
    MutationResultType: grapheneType
        Graphene Type which is returned as a result of mutation
    parentItemName: str
        DbClassModel() should must have an attribute 'parentItemName' and it will be set to value given to mutation method as the parent parameter
        If it is None the createdMutation could be considered as a root item.
    **arguments: Dict[grapheneType]
        contains named arguments for mutation, it can be {'name': graphene.String()}

    Returns
    -------
    resultClass: graphene.Mutation
        subclass of graphene.Mutation class able to perfom a mutation within a grapheneType.
        It can be used as create_new = resultClass.Field()
        
    """

    #assert not parentItemName is None, 'parentItemName must be set to name of item, where parent should be stored'
    # see https://docs.python.org/3/library/types.html

    l = lambda : resultClass
    def mutate(parent, info, **initPars):
        session = extractSession(info)
        if parentItemName is None:
            parameters = {**initPars}
        else:
            parameters = {**initPars, parentItemName: parent}
        result = DbClassModel(**parameters)
        session.add(result)
        session.commit()
        resultClass = l()
        return resultClass(ok=True, result=result)
    
    argumentClass = type('Arguments', (), arguments)
    resultClass = type('Constructor', (Mutation, ), {'Arguments': argumentClass, 'mutate': mutate, 'ok': Boolean(), 'result': MutationResultType})

    return resultClass

