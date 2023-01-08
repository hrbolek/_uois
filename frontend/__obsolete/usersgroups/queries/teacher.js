import { authorizedFetch } from 'generals/authorizedfetch';

/**
 * Retrieves the data from GraphQL API endpoint
 * @param {*} id - identificator
 * @function
 */
 export const TeacherLargeQuery = (id) => 
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
