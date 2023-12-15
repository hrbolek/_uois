import { authorizedFetch } from "../authorizedFetch"
import { authorizedFetch as af} from "@uoisfrontend/shared";

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

export const GroupsByLettersQuery_ = (letters) =>
    af('/gql', {
        body: JSON.stringify(GroupsByLettersQueryJSON(letters))
    })
