import { authorizedFetch } from "@uoisfrontend/shared"
import All from "@uoisfrontend/shared/src/keyedreducers"

export const EventInvitationInsertQueryJSON = (event_id, user_id, invitation_type_id) => ({
    query: `mutation(
      $user_id: ID!
      $event_id: ID!
      $invitation_id: ID!
      $presencetype_id: ID
    ) {
      presenceInsert(presence: {
        userId: $user_id
        eventId: $event_id
        invitationId: $invitation_id
        presencetypeId: $presencetype_id
      }) {
        id
        msg
        presence {
          event {
            __typename
            id
            presences {
              id
              lastchange
              invitationType { id name }
              presenceType { id name }
              user {
                __typename
                id
                name
                surname
                email
              }
            }
          }
        }
      }
    }`,
    variables: {event_id, user_id, invitation_id: invitation_type_id}
})

export const EventInvitationInsert = (event_id, user_id, invitation_type_id) =>
    authorizedFetch('/gql', {
        body: JSON.stringify(EventInvitationInsertQueryJSON(event_id, user_id, invitation_type_id)),
    })

export const EventInvitationInsertAsyncAction = (event_id, user_id, invitation_type_id) => (dispatch, getState) => {
    return (
      EventInvitationInsert(event_id, user_id, invitation_type_id)
        .then(response => response.json())
        .then(
            json => {
                const msg = json?.data?.result?.msg
                if (msg === "ok") {
                    const event = json?.data?.result?.event
                    const action = All.ItemSliceActions.item_update(event)
                    dispatch(action)
                }
                return json
            }
        )
    )
}
