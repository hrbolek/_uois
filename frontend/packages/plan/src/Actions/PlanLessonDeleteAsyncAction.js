import { authorizedFetch } from "@uoisfrontend/shared"
import All from "@uoisfrontend/shared/src/keyedreducers"

export const PlanLessonDeleteQueryJSON = ({plan_id, lesson_id, lastchange}) => ({
    query: `mutation($lesson_id: ID!, $plan_id: ID!, $lastchange: DateTime!) {
      result: plannedLessonRemove(lesson: {id: $lesson_id, planId: $plan_id, lastchange: $lastchange}) 
        {
            id
            msg
            plan { __typename
                id lastchange
                lessons {
                    __typename 
                    id
                    name
                    lastchange
                    type { id name }
                    users { __typename id
                        name surname email
                    }
                    groups { __typename id name }
                    facilities { __typename id name label }
                }
            }
        }
    }`,
    variables: { plan_id, lesson_id: lesson_id, lastchange }
})

export const PlanLessonDeleteQuery = ({plan_id, lesson_id, lastchange}) =>
    authorizedFetch('/gql', {
        body: JSON.stringify(PlanLessonDeleteQueryJSON({plan_id, lesson_id, lastchange})),
    })

export const PlanLessonDeleteAsyncAction = ({plan_id, lesson_id, lastchange}) => (dispatch, getState) => {
    return (
      PlanLessonDeleteQuery({plan_id, lesson_id, lastchange})
        .then(response => response.json())
        .then(
            json => {
                const result = json?.data?.result
                if (result) {
                    const plan = result.plan
                    const action = All.ItemSliceActions.item_update(plan)
                    dispatch(action)
                }
                return json
            }
        )
    )
}
