//import { authorizedFetch } from "../authorizedFetch"
import { authorizedFetch, Queries } from "@uoisfrontend/shared";

const UQ = Queries.UserQuery
export {UQ}
export const UserQueryJSON = (id) => ({
    "query":
        `query($id: ID!) {
            result: userById(id: $id) {
              __typename
              id
              lastchange
              name
              surname
              email
              membership {
                id
                lastchange
                valid
                startdate
                enddate
                group {
                  id
                  name
                }
              }
              roles {
                id
                lastchange
                valid
                startdate
                enddate
                roletype {
                  id
                  name
                  nameEn
                }
                group {
                  id
                  name
                }
              }
          
            }
          }`,
    "variables": {"id": id}
})

export const UserQuery = (id) =>
    authorizedFetch('/gql', {
        body: JSON.stringify(UserQueryJSON(id)),
    })



