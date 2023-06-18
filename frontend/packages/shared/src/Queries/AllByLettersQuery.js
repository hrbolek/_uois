import { authorizedFetch} from "@uoisfrontend/shared";

export const AllByLettersQueryJSON = (letters) => ({
    "query":
        `query($letters: String!) {
            groups: groupByLetters(letters: $letters) {
                id, name
                grouptype {id, name}
            }

            users: userByLetters(letters: $letters) {
                id
                name
                surname
              }
        }`,
    "variables": {"letters": letters}
})

export const AllByLettersQuery = (letters) =>
    authorizedFetch('/gql', {
        body: JSON.stringify(AllByLettersQueryJSON(letters))
    })