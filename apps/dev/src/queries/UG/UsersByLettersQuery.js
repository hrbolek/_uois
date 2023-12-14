import { authorizedFetch } from "queries/authorizedFetch"

export const UsersByLettersJSON = (letters) => (({
    "query":
        `query($letters: String!) {
            users: userByLetters(letters: $letters) {
              id
              name
              surname
            }
        }`,
    "variables": {"letters": letters}
  }))
  
  export const UsersByLettersQuery = (id) =>
      authorizedFetch('/gql', {
          body: JSON.stringify(UsersByLettersJSON(id)),
      })
  