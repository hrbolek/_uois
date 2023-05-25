import { authorizedFetch } from "../authorizedFetch"

export const GroupsByLettersQueryJSON = (letters) => ({
    "query":
        `query($letters: String!) {
            groups: groupByLetters(letters: $letters) {
                id, name
                grouptype {id, name}
            }
        }`,
    "variables": {"letters": letters}
})

export const GroupsByLettersQuery = (letters) =>
    authorizedFetch('/gql', {
        body: JSON.stringify(GroupsByLettersQueryJSON(letters))
    })
