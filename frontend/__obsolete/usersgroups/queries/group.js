import { authorizedFetch } from 'generals/authorizedfetch';

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
                        id, name
                        roles {
                          roletype {
                            name
                          }
                          user {
                            id, name, surname, email
                          }
                        }
                        
                    }
                }`,
            "variables": {"id": id}
        }),
    })