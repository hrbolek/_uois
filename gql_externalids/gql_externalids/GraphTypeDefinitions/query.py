import strawberry

###########################################################################################################################
#
# zde definujte svuj Query model
#
###########################################################################################################################


@strawberry.type(description="""Type for query root""")
class Query:

    from .externalIdGQLModel import external_ids
    external_ids = external_ids

    from .externalIdGQLModel import internal_id
    internal_id = internal_id

    from .externalIdTypeGQLModel import externalidtype_page
    externalidtype_page = externalidtype_page

    from .externalIdTypeGQLModel import externalidtype_by_id
    externalidtype_by_id = externalidtype_by_id

    from .externalIdCategoryGQLModel import externalidcategory_page
    externalidcategory_page = externalidcategory_page