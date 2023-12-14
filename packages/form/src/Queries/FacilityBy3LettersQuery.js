import { authorizedFetch } from "@uoisfrontend/shared";

export const FacilitysBy3LettersQueryJSON = (letters) => ({
    "query":
        `query($letters: String!) {
            result: facilityByLetters(letters: $letters) {
                id
                name
            }
        }`,
    "variables": {"letters": letters}
})

export const FacilitysBy3LettersQuery = (letters) =>
    authorizedFetch('/gql', {
        body: JSON.stringify(FacilitysBy3LettersQueryJSON(letters)),
    })

