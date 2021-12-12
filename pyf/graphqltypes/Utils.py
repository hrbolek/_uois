from graphene import Field, List


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