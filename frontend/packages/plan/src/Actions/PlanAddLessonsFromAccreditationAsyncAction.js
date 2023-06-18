import { authorizedFetch } from "@uoisfrontend/shared"
import All from "@uoisfrontend/shared/src/keyedreducers"


export const PlanGetSemesterDataQueryJSON = (plan_id) => ({
    query: `query($plan_id: ID!) {
        result: planById(id: $id) {
          semester {
            topics {
              id
              name
              lessons {
                id
                type {
                  id
                  name
                }
                count
              }
            }
          }
        }
      }`,
    variables: {plan_id}
})

export const PlanAddLessons = () => ({})

export const PlanAddLessonsFromAccreditationQueryJSON = ({plan_id, name, lessontype_id}) => ({
    query: `mutation($plan_id: ID!, $lessontype_id: ID! $name: String!) {
      result: plannedLessonInsert(lesson: {
          planId: $plan_id
          name: $name
          lessontypeId: $lessontype_id
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
    variables: { plan_id, name, lessontype_id }
})

export const PlanAddLessonsFromAccreditationQuery = ({plan}) =>
    authorizedFetch('/gql', {
        body: JSON.stringify(PlanAddLessonsFromAccreditationQueryJSON({plan})),
    })

export const PlanAddLessonsFromAccreditationAsyncAction = ({plan}) => (dispatch, getState) => {
    return (
      PlanAddLessonsFromAccreditationQuery({plan})
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
