import strawberry

@strawberry.type
class Mutation:
    
    from .externalIdGQLModel import externalid_insert
    externalid_insert = externalid_insert

    from .externalIdGQLModel import externalid_delete
    externalid_delete = externalid_delete

    from.externalIdTypeGQLModel import externaltypeid_insert
    externaltypeid_insert = externaltypeid_insert

    from.externalIdTypeGQLModel import externaltypeid_update
    externaltypeid_update = externaltypeid_update
    
    from .externalIdCategoryGQLModel import externalidcategory_insert
    externalidcategory_insert = externalidcategory_insert

    from .externalIdCategoryGQLModel import externalidcategory_update
    externalidcategory_update = externalidcategory_update
    
    pass