import { authorizedFetch } from "@uoisfrontend/shared";

export const GroupsBy3LettersQueryJSON = (letters) => ({
    "query":
        `query($letters: String!) {
            result: groupByLetters(letters: $letters) {
                id
                name
            }
        }`,
    "variables": {"letters": letters}
})

export const GroupsBy3LettersQuery = (letters) =>
authorizedFetch('/gql', {
    body: JSON.stringify(GroupsBy3LettersQueryJSON(letters)),
})

