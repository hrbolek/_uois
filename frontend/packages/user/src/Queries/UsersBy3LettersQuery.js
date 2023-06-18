import { authorizedFetch } from "@uoisfrontend/shared";

export const UsersBy3LettersQueryJSON = (letters) => ({
    "query":
        `query($letters: String!) {
            result: userByLetters(letters: $letters) {
            id
            name
            surname
            email
            }
        }`,
    "variables": {"letters": letters}
})

export const UsersBy3LettersQuery = (letters) =>
authorizedFetch('/gql', {
    body: JSON.stringify(UsersBy3LettersQueryJSON(letters)),
})

