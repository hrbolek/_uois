import { authorizedFetch } from "@uoisfrontend/shared"
import All from "@uoisfrontend/shared/src/keyedreducers"

export const PlanLessonUpdateQueryJSON = ({lesson}) => ({
    query: `mutation(
        $id: ID! 
        $lastchange: DateTime! 
        $name: String 
        $order: Int
        $length: Int
        $lessontype_id: ID
        ) {
      result: plannedLessonUpdate(lesson: {
        id: $id
        lastchange: $lastchange
        name: $name
        order: $order
        length: $length
        lessontypeId: $lessontype_id
      }) {
        id
        msg
        lesson {
            plan {
                __typename
                id
                lastchange
                lessons {
                    id
                    lastchange
                    name
                    order
                    length
                    type {
                        id
                        name
                    }
                }
            }
        }
      }
    }`,
    variables: {...lesson}
})

export const PlanLessonUpdateQuery = ({lesson}) =>
    authorizedFetch('/gql', {
        body: JSON.stringify(PlanLessonUpdateQueryJSON({lesson})),
    })
    .then(response => response.json())

export const PlanLessonUpdateAsyncAction = ({plan_id, lesson}) => (dispatch, getState) => {
    return (
      PlanLessonUpdateQuery({lesson})
      .then(
            json => {
                const result = json?.data?.result
                if (result) {
                    const plan = result.lesson.plan
                    // const action = All.ItemSliceActions.item_update(plan)
                    const action = All.ItemSliceActions.item_updateAttributeVector({item: plan, vectorname: "lessons"})
                    dispatch(action)
                }
                return json
            }
        )
    )
}
