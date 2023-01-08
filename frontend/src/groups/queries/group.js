import { authorizedFetch } from 'generals/authorizedfetch';

export const GroupBaseQuery = (id) =>
    authorizedFetch('/gql', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        cache: 'no-cache', // *default, no-cache, reload, force-cache, only-if-cached
        redirect: 'follow', // manual, *follow, error
        body: JSON.stringify({
            "query":
                `query ($id: UUID!) {
                    groupById(id: $id) {
                        id, name, valid, lastchange
                        grouptype { id, name }
                        roles {
                            id, user { id, name,surname, email }, roletype { id, name}
                        }
                        subgroups {
                            id, name, valid, lastchange, grouptype { id, name }
                            roles {
                                id, user { id, name,surname, email }, roletype { id, name}
                            }
                        }
                    }
                }`,
            "variables": {"id": id}
        }),
    })

export const UniversityLargeQuery = GroupBaseQuery

export const GroupLargeQuery = (id) =>
    authorizedFetch('/gql', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        cache: 'no-cache', // *default, no-cache, reload, force-cache, only-if-cached
        redirect: 'follow', // manual, *follow, error
        body: JSON.stringify({
            "query":
                `query ($id: UUID!) {
                    groupById(id: $id) {
                        id, name, valid, lastchange
                        grouptype { id, name }
                        roles {
                            id, user { id, name,surname, email }
                        }
                        memberships {
                            id, valid, user { 
                                id, name, surname, email
                            }
                        }
                        subgroups {
                            id, name, valid, lastchange, grouptype { id, name }
                        }
                    }
                }`,
            "variables": {"id": id}
        }),
    })

export const DepartmentLargeQuery = (id) =>
    authorizedFetch('/gql', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        cache: 'no-cache', // *default, no-cache, reload, force-cache, only-if-cached
        redirect: 'follow', // manual, *follow, error
        body: JSON.stringify({
            "query":
                `query ($id: UUID!) {
                    groupById(id: $id) {
                        id, name, valid, lastchange
                        grouptype { id, name }
                        roles {
                            id, user { id, name,surname, email }, roletype { id, name}
                        }
                        memberships {
                            id, valid, user { 
                                id, name, surname, email
                            }
                        }
                        subgroups {
                            id, name, valid, lastchange, grouptype { id, name }
                        }
                        mastergroup {
                            id, name, valid
                            grouptype { id, name }

                            mastergroup {
                                id, name, valid
                                grouptype { id, name }
                            }
                        }
                    }
                }`,
            "variables": {"id": id}
        }),
    })

export const FacultyLargeQuery = (id) =>
    authorizedFetch('/gql', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        cache: 'no-cache', // *default, no-cache, reload, force-cache, only-if-cached
        redirect: 'follow', // manual, *follow, error
        body: JSON.stringify({
            "query":
                `query ($id: UUID!) {
                    groupById(id: $id) {
                        id, name, valid, lastchange
                        grouptype { id, name }
                        roles {
                            id, user { id, name,surname, email }, roletype { id, name}
                        }
                        subgroups {
                            id, name, valid, lastchange, grouptype { id, name }
                        }
                        mastergroup {
                            id, name, valid
                            grouptype { id, name }
                        }
                    }
                }`,
            "variables": {"id": id}
        }),
    })



const variablesToUpdate = ['valid', 'name', 'lastchange']
export const GroupUpdateQuery = (group) => {
    const limitedgroup = {}
    for(const variable of variablesToUpdate) {
        if (variable in group) {
            limitedgroup[variable] = group[variable]
        }
    }

    return authorizedFetch('/gql', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        cache: 'no-cache', // *default, no-cache, reload, force-cache, only-if-cached
        redirect: 'follow', // manual, *follow, error
        body: JSON.stringify({
            "query":
                `query ($id: UUID!, $data: GroupUpdateGQLModel!) {
                    groupById(id: $id) {
                        editor {
                            update(group: $data) {
                                result
                                group {
                                    id, name, valid, lastchange
                                    grouptype { id, name }
                                    memberships {
                                        id, valid, user { 
                                            id, name, surname, email
                                        }
                                    }
                                }
                            }
                        }
                    }
                }`,
            "variables": {"id": group.id, "data": limitedgroup}
        }),
    })
}

export const GroupAddRoleQuery = (group, role, user) => {
    return authorizedFetch('/gql', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        cache: 'no-cache', // *default, no-cache, reload, force-cache, only-if-cached
        redirect: 'follow', // manual, *follow, error
        body: JSON.stringify({
            "query":
                `query ($id: UUID!, $role_id: UUID!, $user_id: UUID!) {
                    groupById(id: $id) {
                        editor {
                            add_role(role_id: $role_id, user_id: $user_id) {
                                id
                            }
                        }
                    }
                }`,
            "variables": {"id": group.id, "$role_id": role.id, "$user_id": user.id}
        }),
    })
}

export const GroupAssignSubgroupQuery = (group, subgroup) => {
    return authorizedFetch('/gql', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        cache: 'no-cache', // *default, no-cache, reload, force-cache, only-if-cached
        redirect: 'follow', // manual, *follow, error
        body: JSON.stringify({
            "query":
                `query ($id: UUID!, $subgroup_id: UUID!) {
                    groupById(id: $id) {
                        editor {
                            assign_subgroup(subgroup_id: $subgroup_id) {
                                id
                            }
                        }
                    }
                }`,
            "variables": {"id": group.id, "$subgroup_id": subgroup.id}
        }),
    })
}

export const GroupAddMembershipQuery = (group, user) => {
    return authorizedFetch('/gql', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        cache: 'no-cache', // *default, no-cache, reload, force-cache, only-if-cached
        redirect: 'follow', // manual, *follow, error
        body: JSON.stringify({
            "query":
                `query ($id: UUID!, $user_id: UUID!) {
                    groupById(id: $id) {
                        editor {
                            add_membership(user_id: $user_id) {
                                id
                            }
                        }
                    }
                }`,
            "variables": {"id": group.id, "$user_id": user.id}
        }),
    })
}

export const GroupInvalidateMembershipQuery = (group, membership) => {
    return authorizedFetch('/gql', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        cache: 'no-cache', // *default, no-cache, reload, force-cache, only-if-cached
        redirect: 'follow', // manual, *follow, error
        body: JSON.stringify({
            "query":
                `query ($id: UUID!, $user_id: UUID!) {
                    groupById(id: $id) {
                        editor {
                            invalidate_membership(membership_id: $membership_id) {
                                id
                            }
                        }
                    }
                }`,
            "variables": {"id": group.id, "$membership_id": membership.id}
        }),
    })
}