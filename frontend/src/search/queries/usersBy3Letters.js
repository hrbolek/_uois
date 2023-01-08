import { authorizedFetch } from 'generals/authorizedfetch';

export const queryUsersByLetters = (letters) => 
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
                    userByLetters(letters: $letters) {
                    id
                    name
                    surname
                    }
                }`,
            "variables": {"letters": letters}
        }),
    })
