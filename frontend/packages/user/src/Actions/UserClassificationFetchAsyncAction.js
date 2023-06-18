import { authorizedFetch } from "@uoisfrontend/shared"
import React, { useEffect } from "react"
import Table from "react-bootstrap/Table"
import { useDispatch } from "react-redux"

import All from "@uoisfrontend/shared/src/keyedreducers"
import Button from "react-bootstrap/Button"

export const UserClassificationQueryJSON = (id) => ({
    query: `
    query ($id: ID!) {
        result: userById(id: $id) {
            id
            classifications {
                id
                lastchange
                semester { id}
                level{id name}
                order
                date
            }
        }
      }
    `,
    variables: {id}
})

export const UserClassificationQuery = (id) => 
    authorizedFetch('/gql', {
        body: JSON.stringify(UserClassificationQueryJSON(id))
    })

export const UserClassificationFetchAsyncAction = ({id}) => (dispatch, getState) => {
    UserClassificationQuery(id)
    .then(response => response.json())
    .then(json => {
        const result = json?.data?.result
        if (result) {
            const action = All.ItemSliceActions.item_update(result)
            dispatch(action)
        }
    })

}