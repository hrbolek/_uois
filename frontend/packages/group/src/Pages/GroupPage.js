import { useEffect, useState } from "react"
import { Navigate, useParams } from "react-router-dom"
import { useSelector, useDispatch } from "react-redux/"

import { GroupCard } from "../Components/GroupCard"
import { GroupFetchAsyncAction } from "../Actions/GroupFetchAsyncAction"
import { CheckGQLError, MsgAddAction, MsgFlashAction, useFreshItem } from "@uoisfrontend/shared"
import { GroupMembersFetchAsyncAction } from "../Actions/GroupMembersFetchAsyncAction"
import { Col } from "react-bootstrap"
import { Row } from "react-bootstrap"
import { GroupSearch, GroupSugestionLink } from "../Components/GroupSearch"
import { useMemo } from "react"

// const fakePromise = {
//     then: (json) => new Promise((resolve, reject) => resolve(json)),
//     finally: (json) => new Promise((resolve, reject) => resolve(json)),
//     catch: (json) => new Promise((resolve, reject) => reject(json))
// }
// const fakePromise = {
//     then: (json) => new Promise((resolve, reject) => null),
//     finally: (json) => new Promise((resolve, reject) => null),
//     catch: (json) => new Promise((resolve, reject) => null)
// }
// export const useFreshItem_ = (oldItemWithId, AsyncAction) => {
//     const id = oldItemWithId.id
//     const dispatch = useDispatch()
//     const items = useSelector(state => state.items)
//     const result = items[oldItemWithId.id]
//     // const p = new Promise()
//     const [resultPromise, setPromise] = useState(fakePromise)//() => new Promise())

//     useEffect(
//         () => {
//             const controller = new AbortController();
//             const signal = controller.signal;
        
//             const presult = dispatch(AsyncAction({id}, signal))
//                 // .then(
//                 //     CheckGQLError({
//                 //         "ok": (json) => dispatch(MsgFlashAction({ title: "Nahrání skupiny úspěšné" })),
//                 //         "fail": (json) => dispatch(MsgAddAction({ title: "Chyba " + JSON.stringify(json) })),
//                 //     })
//                 // )
//                 .then(json => {
//                     console.log("got", json)
//                     return json
//                 })
//             // if (group?.grouptype?.id === "cd49e152-610c-11ed-9f29-001a7dda7110") {
//             //     //je Univerzita
//             // } else {
//             //     //neni Univerzita
//             //     dispatch(GroupMembersFetchAsyncAction(id))
//             //         .then(
//             //             CheckGQLError({
//             //                 "ok": (json) => dispatch(MsgFlashAction({ title: "Nahrání členů skupiny úspěšné" })),
//             //                 "fail": (json) => dispatch(MsgAddAction({ title: "Chyba " + JSON.stringify(json) })),
//             //             })
//             //         )
//             // }
//             setPromise(presult)

//             return () => {
//                 controller.abort()
//             }
//         },
//         [id]
//     )
//     return [result, resultPromise]
// }

// const extend = (what, extension) => (json) => {
//     console.log("extend.json", json)
//     console.log("extend.what", what)
//     const asyncAction = (dispatch, getState) => {
        
//         const result = what(json)
//         console.log("extend.dispatch", result)
//         // return result
//         return null
//     }
//     return asyncAction
//     // .then(
//     //     json => dispatch(extension(json))
//     // )
// }
export const GroupPageNoUniversity = () => <GroupPage query={GroupMembersFetchAsyncAction} />

export const GroupPage = ({query=GroupFetchAsyncAction}) => {
    const dispatch = useDispatch()

    const { id } = useParams()
    
    const [group, updateDone] = useFreshItem({id: id}, 
        GroupFetchAsyncAction)

    updateDone
    .then(
        CheckGQLError({
            "ok": (json) => dispatch(MsgFlashAction({ title: "Nahrání skupiny úspěšné" })),
            "fail": (json) => dispatch(MsgAddAction({ title: "Chyba " + JSON.stringify(json) })),
        })
    )
    
    if (group){
        if (group?.grouptype.id === "cd49e153-610c-11ed-bf19-001a7dda7110") {
            return (<Navigate to={"/ui/faculty/" + group.id} replace={true} />)
        }
        if (group?.grouptype.id === "cd49e155-610c-11ed-844e-001a7dda7110") {
            return (<Navigate to={"/ui/department/" + group.id} replace={true} />)
        }
        if (group?.grouptype.id !== "cd49e152-610c-11ed-9f29-001a7dda7110") {
            return (<Navigate to={"/ui/groups/nouni/" + group.id} replace={true} />)
        } else {
            return (
                <>
                {/* <Row>
                    <Col>
                        <div className="float-end">
                            <GroupSearch Suggestion={GroupSugestionLink} />
                        </div>
                    </Col>
                </Row> */}
                <Row>
                    <Col>
                        <GroupCard group={group} />
                    </Col>
                </Row>
                </>
            )
        }
        
    } else {
        return <>Loading group</>
    }
}