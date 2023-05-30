import strawberry
@strawberry.type(description="""Root query""")
class Query:

    from .tagEntityModel import preference_entities
    preference_entities = preference_entities
    
    from .tagModel import preference_tags
    preference_tags = preference_tags
    
    from .tagEntityModel import preference_entity_tags
    preference_entity_tags = preference_entity_tags
    pass