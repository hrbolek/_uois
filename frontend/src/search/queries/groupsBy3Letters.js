import { authorizedFetch } from 'generals/authorizedfetch';

export const queryGroupsByLetters = (letters) => 
    authorizedFetch('/gql', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        cache: 'no-cache', // *default, no-cache, reload, force-cache, only-if-cached
        redirect: 'follow', // manual, *follow, error
        body: JSON.stringify({
            "query":
                `query($letters: String!) {
                    groupByLetters(letters: $letters) {
                        id, name
                        grouptype {id, name}
                    }
                }`,
            "variables": {"letters": letters}
        }),
    })