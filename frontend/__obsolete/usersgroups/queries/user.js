import { authorizedFetch } from 'generals/authorizedfetch'

const userUpdateItem = (itemName) => (id, itemValue) => {
    const variables = {"id": id}
    variables[itemName] = itemValue
    return authorizedFetch('/gql', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        cache: 'no-cache', // *default, no-cache, reload, force-cache, only-if-cached
        redirect: 'follow', // manual, *follow, error
        body: JSON.stringify({
            "query":
                `query ($id: UUID!) {
                userById(id: $id) {
                    editor { 
                        id 
                        update(name: $name)
                    }
                }
            }`,
            "variables": variables
        }),
    })
}

//export const userUpdateNameQuery = userUpdateItem('name')
export const userUpdateNameQuery = (id, name) => 
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
                userById(id: $id) {
                    editor { 
                        id 
                        update(name: $name)
                    }
                }
            }`,
         "variables": {"id": id, "name": name}
     }),
 })

 export const userUpdateSurnameQuery = (id, surname) => 
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
                userById(id: $id) {
                    editor { 
                        id 
                        update(name: $name)
                    }
                }
            }`,
         "variables": {"id": id, "surname": surname}
     }),
 })


const variablesToUpdate = ['name', 'surname', 'email', 'lastchange']
export const userUpdateQuery = (user) => {
    let limitedUser = {}
    
    for(const variable of variablesToUpdate) {
        if (variable in user) {
            limitedUser[variable] = user[variable]
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
                `query ($id: UUID!, $data: UserUpdateGQLModel!) {
                    userById(id: $id) {
                        editor { 
                            update(data: $data) {
                                result
                                user { id, name, surname, email, lastchange }
                            }
                        }
                    }
                }`,
            "variables": {"id": user.id, "data": limitedUser}
        }),
    })
}

/**
 * Retrieves the data from GraphQL API endpoint
 * @param {*} id - identificator
 * @function
 */
 export const userLargeQuery = (id) => 
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
                userById(id: $id) {
                    editor { id }
                    id, name, surname, email, lastchange
                    externalIds { typeName, outerId }
                    membership {
                        valid
                        group {
                            id, name
                            grouptype { id, name, nameEn }
                        }
                    }
                    roles {
                        id
                        roletype { id, name }
                        group {
                            id, name
                            grouptype { id, name, nameEn }
                        }
                    }
                }
            }`,
         "variables": {"id": id}
     }),
 })
