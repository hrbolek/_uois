import strawberry

@strawberry.type
class Mutation:
    
    from .tagModel import tag_insert
    tag_insert = tag_insert

    from .tagModel import tag_update
    tag_update = tag_update

    from .tagModel import tag_delete
    tag_delete = tag_delete

    from .tagEntityModel import tag_add_to_entity
    tag_add_to_entity = tag_add_to_entity

    from .tagEntityModel import tag_remove_from_entity
    tag_remove_from_entity = tag_remove_from_entity
    pass