// import { EventQuery } from "@uoisfrontend/shared/src/Queries/EventQuery"
import { authorizedFetch } from "@uoisfrontend/shared"
import All from "@uoisfrontend/shared/src/keyedreducers"

export const FormUpdateItemQueryJSON = ({item}) => ({
    query: `
        mutation($id: ID! $lastchange: DateTime! $value: String!) {
          result:  formItemUpdate(item: {id: $id lastchange: $lastchange value: $value}) {
            id
            msg
            item {
              id
              lastchange
              value
              part {
                section {
                  form {
                    __typename
                    id
                    lastchange
                    name
                    valid
                    type {
                      id 
                      name
                    }
                    sections {
                      id
                      name
                      lastchange
                      order
                      parts {
                        id
                        name
                        lastchange
                        order
                        items {
                          id
                          name
                          order
                          lastchange
                          value
                          type {
                            id 
                            name
                          }
                        }
                      }
                    }
                  }
                }
              }
            }
          }
        }`,

    "variables": {...item}
})

export const FormUpdateItemQuery = ({item}) => 
    authorizedFetch('/gql', {
        body: JSON.stringify(FormUpdateItemQueryJSON({item})),
    })

export const FormUpdateItemAsyncAction = ({item}) => (dispatch, getState) => {
    console.log("FormUpdateItemAsyncAction", item)
    return (
        FormUpdateItemQuery({item})
        .then(response => response.json())
        .then(
            json => {
                const result = json?.data?.result
                if (result) {
                    const action = All.ItemSliceActions.item_update(result)
                    dispatch(action)
                }
                return json
            }
        )
    )
}
