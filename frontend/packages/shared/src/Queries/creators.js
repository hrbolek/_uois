import { authorizedFetch } from "./authorizedFetch"
import { ItemActions } from "../keyedreducers"

const ResponseFromQuery = (Query) => (item) => {
    // console.log("ResponseFromQuery", item)
    // console.log("ResponseFromQuery", Query)
    const body = JSON.stringify(Query(item))
    // console.log("ResponseFromQuery", body)
    const result = authorizedFetch('', {body})
    .then(
        response => response.json()
    )
    // .then(
    //     json => {
    //         console.log("ResponseFromQuery got", json)
    //         return json
    //     }
    // )
    return result
}

export const CreateFetchQuery = ResponseFromQuery

export const CreateAsyncActionFromIdQuery = (Query) => (item) => (dispatch, getState) => {
    return ResponseFromQuery(Query)(item)
    .then(
        json => {
            const fetched = json?.data?.result
            if (fetched) {
                dispatch(ItemActions.item_update(fetched))
            }
            return json
        }
    )
}

export const CreateAsyncActionFromPageQuery = (Query) => (item) => (dispatch, getState) => {
    return ResponseFromQuery(Query)(item)
    .then(
        json => {
            const result = json?.data?.result
            if (result) {
                result.forEach(item => {
                    dispatch(ItemActions.item_update(item))
                });
            }
        }
    )
}


// json => {
//     const result = json?.data?.result
//     if (result) {
//         result.forEach(sensor => {
//             dispatch(ItemActions.item_update(sensor))
//         });
//     }
// }

