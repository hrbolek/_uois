


import { CheckGQLError, MsgAddAction, MsgFlashAction, authorizedFetch } from "@uoisfrontend/shared"
import All from "@uoisfrontend/shared/src/keyedreducers"
import { useEffect } from "react"
import { useDispatch, useSelector } from "react-redux"

export const PresenceTypesQueryJSON = () => ({
    query: `{
        result: presenceTypePage {
          id
          name
          nameEn
        }
      }`
})

export const PresenceTypesFetchQuery = () => 
    authorizedFetch('/gql', {
        body: JSON.stringify(PresenceTypesQueryJSON())
    })

export const PresencesItemStoreId = "4549709e-03f1-41d4-95dc-80d0c535ea65"

export const PresenceTypesFetchAsyncAction = () => (dispatch, getState) => {
    
    return (
        PresenceTypesFetchQuery()
        .then(response => response.json())
        .then(json=> {
            const result = json?.data?.result
            if (result) {
                const action = All.ItemSliceActions.item_update({id: PresencesItemStoreId, presencetypes: result})
                dispatch(action)
                // console.log("PresenceTypesFetchAsyncAction", result)
            }
            return json
        })
    )
}

const mappedColors = {
    "466398c6-a79c-11ed-b76e-0242ac110002": " bg-success text-white",
    "4663988a-a79c-11ed-b76e-0242ac110002": " bg-danger text-white",
}

export const PresenceTypeSelect = ({ value, onSelect }) => {
    const items = useSelector(state => state.items)
    const dispatch = useDispatch()
    const presencetypes = items[PresencesItemStoreId]
    
    useEffect(
        () => {
            if (presencetypes) {
                
            } else {
                dispatch(PresenceTypesFetchAsyncAction())
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
    const className = mappedColors[value] || " bg-white"
    if (presencetypes) {
        return (
            <select className={"form-control" + className} onChange={onChange} value={value}>
                {presencetypes.presencetypes.map(
                    presencetype => <option className="text-dark" style={{backgroundColor: "Ivory"}} key={presencetype.id} value={presencetype.id}>{presencetype.name}</option>
                )}
            </select>
        )
    } else {
        return null
    }
};


export const PresenceUpdateQueryJSON = (presence) => ({
    query: `mutation($id: ID! $lastchange: DateTime! $presencetype_id: ID $invitationtype_id: ID) {
        result: presenceUpdate(presence: {
          id: $id
          lastchange: $lastchange
          presencetypeId: $presencetype_id
          invitationId: $invitationtype_id
        }){
          id
          msg
          presence {
            event {
              id
              name
              presences {
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
      variables: {
        ...presence, 
        presencetype_id: presence.presencetype_id, 
        invitationtype_id: presence.invitationtype_id
    }
})

export const PresenceUpdateFetchQuery = (presence) => 
    authorizedFetch('/gql', {
        body: JSON.stringify(PresenceUpdateQueryJSON(presence))
    })

export const PresenceUpdateAsyncAction = ({presence}) => (dispatch, getState) => {
    return (
        PresenceUpdateFetchQuery(presence)
        .then(response => response.json())
        .then(json=> {
            const result = json?.data?.result
            if (result) {
                // console.log("PresenceUpdateFetchAsyncAction", result)
                const event = result?.presence?.event
                if (event) {
                    const action = All.ItemSliceActions.item_update({...event})
                dispatch(action)
                // console.log("PresenceUpdateFetchAsyncAction", result)
                }
                
            }
            return json
        })
    )
}

export const EventPresenceSelect = ({ presence }) => {
    const dispatch = useDispatch()
    const onSelect = (value) => {
        const newPresence = {...presence, presencetype_id: value}
        // console.log("EventPresenceSelect.onSelect", value, newPresence)
        dispatch(PresenceUpdateAsyncAction({presence: newPresence}))
        .then(
            CheckGQLError({
                "ok": () => dispatch(MsgFlashAction({title: "Změna ok"})),
                "fail": (json) => dispatch(MsgAddAction({title: "Změna se nepovedla\n " + JSON.stringify(json)}))
            })
        )

    }
    return (
        <PresenceTypeSelect value={presence.presenceType?.id} onSelect={onSelect}/>
    )
};
