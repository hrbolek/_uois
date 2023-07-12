import { authorizedFetch } from "@uoisfrontend/shared"
import All from "@uoisfrontend/shared/src/keyedreducers"

export const LessonRemoveGroupQueryJSON = ({lesson_id, group_id}) => ({
    query: `mutation($group_id: ID! $lesson_id: ID!) {
      result: plannedLessonGroupDelete(grouplesson: {groupId: $group_id, planlessonId: $lesson_id }) {
        id
        msg
        lesson {
            plan {
                __typename
                id
                lastchange
                lessons {
                    __typename 
                    id
                    name
                    lastchange
                    order
                    length
                    type { id name }
                    users {
                        __typename
                        id
                        name
                        surname
                        email
                    }
                    groups {
                        __typename
                        id
                        name
                    }
                    facilities {
                        __typename
                        id
                        name
                        label
                    }
                }
            }
        }
      }
    }`,
    variables: {lesson_id, group_id}
})

export const LessonRemoveGroupQuery = ({group_id, lesson_id}) =>
    authorizedFetch('/gql', {
        body: JSON.stringify(LessonRemoveGroupQueryJSON({lesson_id, group_id})),
    })

export const LessonRemoveGroupAsyncAction = ({plan_id, group_id, lesson_id}) => (dispatch, getState) => {
    return (
      LessonRemoveGroupQuery({group_id, lesson_id})
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
