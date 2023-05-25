import { useEffect } from "react"
import { useParams } from "react-router-dom"
import { useSelector } from "react-redux"

import { useActions } from "./AppProvider"
import { UserCard } from "../components/UG/UserCard"
import { UserEditCard } from "../components/UG/UserEditCard"


export const UserPage = () => {
    const id = useParams().id
    const actions = useActions()
    const users = useSelector(state => state.items)
    const user = users[id]
    
    useEffect(
        () => {
            //console.log("useEffect", _id)
            
            actions?.onUserFetchAsync(id)
            .then(json => {
                if (json?.errors) {
                    // console.log(json?.errors)
                    actions.onMsgFlashAsync({title: 'error: ' + JSON.stringify(json.errors), variant: "danger"})
                } else {
                    // console.log(json?.data?.result)
                    actions.onMsgFlashAsync({title: 'user loaded successfully', variant: "success"})
                }
            })
        },
        [id]
    )

    if (user) {
        return (
            <UserCard user={user} actions={actions} />
        )    
    } else {
        return <div>Loading User {JSON.stringify(id)}...</div>
    }
   
}

export const UserEditPage = () => {
    const id = useParams().id
    const actions = useActions()
    const users = useSelector(state => state.items)
    const user = users[id]
    
    useEffect(
        () => {
            //console.log("useEffect", _id)
            
            actions?.onUserFetchAsync(id)
            .then(json => {
                if (json?.errors) {
                    console.log(json?.errors)
                    actions.onMsgFlashAsync({title: 'error: ' + JSON.stringify(json.errors), variant: "danger"})
                } else {
                    console.log(json?.data?.result)
                    actions.onMsgFlashAsync({title: 'user loaded successfully', variant: "success"})
                }
            })
        },
        [id]
    )

    if (user) {
        return (
            <UserEditCard user={user} actions={actions} />
        )    
    } else {
        return <div>Loading User {JSON.stringify(id)}...</div>
    }
   
}