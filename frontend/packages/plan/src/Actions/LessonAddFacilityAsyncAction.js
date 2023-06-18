import { authorizedFetch } from "@uoisfrontend/shared"
import All from "@uoisfrontend/shared/src/keyedreducers"

export const LessonAddFacilityQueryJSON = ({lesson_id, user_id}) => ({
    query: `mutation($user_id: ID! $lesson_id: ID!) {
      result: plannedLessonFacilityAdd(userlesson: {userId: $user_id, planlessonId: $lesson_id }) {
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
    variables: {lesson_id, user_id}
})

export const LessonAddFacilityQuery = ({user_id, lesson_id}) =>
    authorizedFetch('/gql', {
        body: JSON.stringify(LessonAddFacilityQueryJSON({lesson_id, user_id})),
    })

export const LessonAddFacilityAsyncAction = ({plan_id, user_id, lesson_id}) => (dispatch, getState) => {
    return (
      LessonAddFacilityQuery({user_id, lesson_id})
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
