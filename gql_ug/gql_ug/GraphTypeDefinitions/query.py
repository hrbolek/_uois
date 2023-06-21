import strawberry

@strawberry.type(description="""Type for query root""")
class Query:

    from .userGQLModel import user_by_id
    user_by_id = user_by_id

    from .userGQLModel import user_page
    user_page = user_page

    from .userGQLModel import user_by_letters
    user_by_letters = user_by_letters

    from .groupGQLModel import group_by_id
    group_by_id = group_by_id

    from .groupGQLModel import group_page
    group_page = group_page

    from .groupGQLModel import group_by_letters
    group_by_letters = group_by_letters

    from .roleTypeGQLModel import role_type_by_id
    role_type_by_id = role_type_by_id

    from .roleTypeGQLModel import role_type_page
    role_type_page = role_type_page

    from .roleCategoryGQLModel import role_category_by_id
    role_category_by_id = role_category_by_id

    from .roleCategoryGQLModel import role_category_page
    role_category_page = role_category_page

    from .groupTypeGQLModel import group_type_by_id
    group_type_by_id = group_type_by_id

    from .groupTypeGQLModel import group_type_page
    group_type_page = group_type_page