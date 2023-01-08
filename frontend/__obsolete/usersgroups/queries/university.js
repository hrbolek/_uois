import { authorizedFetch } from 'generals/authorizedfetch';

export const UniversityLargeQuery = (id) =>
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
                        id, name
                        roles {
                          roletype {
                            name
                          }
                          user {
                            id, name, surname, email
                          }
                        }
                        
                        subgroups {
                          id, name
                          grouptype {
                            id, name
                          }
                          roles {
                            id
                            roletype {
                                id, name
                            }
                            user {
                                id, name, surname, email
                            }
                          }
                        }
                    }
                }`,
            "variables": {"id": id}
        }),
    })