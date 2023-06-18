import { useEffect, useState } from "react"
import { UserQuery } from "../Queries/UserQuery"
import { CheckGQLError } from "@uoisfrontend/shared"
import { UserCard } from "../Components/UserCard"
import { useSelector } from "react-redux"
export const UserPageS = ({id}) => {
    //const [user, setUser] = useState(null)
    const items = useSelector(state => state.items)
    const user = items[id] || {id}
    useEffect(
        () => {
            console.log("UserPageS useEffect", id)
            UserQuery(id)
            .then(response => response.json())
            .then( CheckGQLError({
                errors: (e) => console.log(e),
                ok: () => console.log("UserPageS ok"),
                fail: () => console.log("UserPageS fail")
            }) )
            .then(json => {
                if (json?.errors) {
                } else {
                    const _user = json?.data?.result
                    //setUser(_user)
                    console.log("UserPageS useEffect", JSON.stringify(json))
                }
            })
        },
        [id]
    )

    if (user) {
        return (
             <UserCard user={user} />
        )    
    } else {
        return <div>Loading User {JSON.stringify(id)}...</div>
    }  
}