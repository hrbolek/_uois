


import { CheckGQLError, MsgAddAction, MsgFlashAction, authorizedFetch } from "@uoisfrontend/shared"
import All from "@uoisfrontend/shared/src/keyedreducers"
import { useEffect } from "react"
import { useDispatch, useSelector } from "react-redux"
import { PresenceUpdateAsyncAction } from "./EventPresenceSelect"

export const InvitationTypesQueryJSON = () => ({
    query: `{
        result: invitationTypePage {
          id
          name
          nameEn
        }
      }`
})

export const InvitationTypesFetchQuery = () => 
    authorizedFetch('/gql', {
        body: JSON.stringify(InvitationTypesQueryJSON())
    })

export const InvitationsItemStoreId = "96b4a4eb-95b8-47e9-a7e5-2ef2ad921f38"

export const InvitationTypesFetchAsyncAction = () => (dispatch, getState) => {
    
    return (
        InvitationTypesFetchQuery()
        .then(response => response.json())
        .then(json=> {
            const result = json?.data?.result
            if (result) {
                const action = All.ItemSliceActions.item_update({id: InvitationsItemStoreId, invitationtypes: result})
                dispatch(action)
                // console.log("InvitationTypesFetchAsyncAction", result)
            }
            return json
        })
    )
}

const mappedColors = {
    "e871403c-a79c-11ed-b76e-0242ac110002": " bg-success text-white",
    "e8714104-a79c-11ed-b76e-0242ac110002": " bg-danger text-white",
}

export const InvitationTypeSelect = ({ value, onSelect }) => {
    const items = useSelector(state => state.items)
    const dispatch = useDispatch()
    const invitationtypes = items[InvitationsItemStoreId]
    useEffect(
        () => {
            if (invitationtypes) {

            } else {
                dispatch(InvitationTypesFetchAsyncAction())
                .then(json => json)
            }
        }
    )
    const onChange = (e) => {
        const value = e.target.value
        if (onSelect) {
            onSelect(value)
        }
    }
    const value_ = value || ""
    const className = mappedColors[value] || ""
    if (invitationtypes) {
        return (
            <select className={"form-control" + className} onChange={onChange} value={value_}>
                {value?"":<option className="text-dark" key={0} >--- ? ---</option>}
                {invitationtypes.invitationtypes.map(
                    invitationtype => <option className="text-dark" key={invitationtype.id} value={invitationtype.id}>{invitationtype.name}</option>
                )}
            </select>
        )
    } else {
        return <>?</>
    }
};

export const InvitationUpdateQueryJSON = (invitation) => ({
    query: `mutation($id: ID! $lastchange: DateTime! $invitationtype_id: ID!) {
        result: invitationUpdate(invitation: {
          id: $id
          lastchange: $lastchange
          invitationtypeId: $invitationtype_id
        }){
          id
          msg
          invitation {
            event {
              id
              name
              invitations {
                id
                lastchange
                user {
                  id
                  name
                  surname
                  email
                }
                invitationType { id name }
                presenceType { id name }
                
              }
            }
          }
        }
      }`,
      variables: {...invitation, invitationtype_id: invitation.invitationtype_id}
})

export const InvitationUpdateFetchQuery = (invitation) => 
    authorizedFetch('/gql', {
        body: JSON.stringify(InvitationUpdateQueryJSON(invitation))
    })

   
export const InvitationUpdateAsyncAction = ({invitation}) => (dispatch, getState) => {
    return (
        InvitationUpdateFetchQuery(invitation)
        .then(response => response.json())
        .then(json=> {
            const result = json?.data?.result
            if (result) {
                // console.log("InvitationUpdateFetchAsyncAction", result)
                const event = result?.invitation?.event
                if (event) {
                    const action = All.ItemSliceActions.item_update({...event})
                dispatch(action)
                // console.log("InvitationUpdateFetchAsyncAction", result)
                }
                
            }
            return json
        })
    )
}


export const EventInvitationSelect = ({ presence }) => {
    const dispatch = useDispatch()
    const onSelect = (value) => {
        const newPresence = {...presence, invitationtype_id: value}
        // console.log("EventInvitationSelect.onSelect", value, newPresence)
        dispatch(PresenceUpdateAsyncAction({presence: newPresence}))
        .then(
            CheckGQLError({
                "ok": () => dispatch(MsgFlashAction({title: "Změna ok"})),
                "fail": (json) => dispatch(MsgAddAction({title: "Změna se nepovedla\n " + JSON.stringify(json)}))
            })
        )

    }
    return (
        <InvitationTypeSelect value={presence.invitationType?.id} onSelect={onSelect}/>
    )
};
