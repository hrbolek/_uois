import { authorizedFetch } from "@uoisfrontend/shared"
import All from "@uoisfrontend/shared/src/keyedreducers"

export const PlanLessonInsertQueryJSON = ({plan_id, name, lessontype_id, order, length}) => ({
    query: `mutation($plan_id: ID!, $lessontype_id: ID! $name: String! $order: Int $length: Int) {
      result: plannedLessonInsert(lesson: {
          planId: $plan_id
          name: $name
          lessontypeId: $lessontype_id
          order: $order
          length: $length
        }) {
          id
          msg
          lesson {
       
            plan { __typename
                id lastchange
                lessons {
                    __typename 
                    id
                    name
                    lastchange
                    order
                    length
                    type { id name }
                    users { __typename id
                        name surname email
                    }
                    groups { __typename id name }
                    facilities { __typename id name label }
                }
            }
          }
      }
    }`,
    variables: { plan_id, name, lessontype_id, order, length }
})

export const PlanLessonInsertQuery = ({plan_id, name, lessontype_id, order, length}) =>
    authorizedFetch('/gql', {
        body: JSON.stringify(PlanLessonInsertQueryJSON({plan_id, name, lessontype_id, order, length})),
    })

export const PlanLessonInsertAsyncAction = ({plan_id, name, lessontype_id, order, length}) => (dispatch, getState) => {
    return (
      PlanLessonInsertQuery({plan_id, name, lessontype_id, order, length})
        .then(response => response.json())
        .then(
            json => {
                const result = json?.data?.result
                if (result) {
                    const plan = result.lesson.plan
                    const action = All.ItemSliceActions.item_update(plan)
                    dispatch(action)
                }
                return json
            }
        )
    )
}
