import Row from "react-bootstrap/Row"
import Col from "react-bootstrap/Col"
import { CheckGQLError, Link, MsgAddAction, MsgFlashAction, useFreshItem } from "@uoisfrontend/shared"
import { UserFetchAsyncAction } from "../../../../user/src/Actions/UserFetchAsyncAction"
import { UserSearch } from "@uoisfrontend/user"
import { MasterItem } from "./MasterItem"
import { useState } from "react"
import { useDispatch } from "react-redux"
import { FormUpdateItemAsyncAction } from "../../Actions/FormUpdateItemAsyncAction"
// import { UserFetchAsyncAction } from "@uoisfrontend/user/UserFetchAsyncAction"

export const StudentItemEdit = ({item}) => {
    const [user] = useFreshItem({id: item.value}, UserFetchAsyncAction)
    const [selected, setSelected] = useState(item.value)
    const dispatch = useDispatch()
    const onSelect = (value) => {
        setSelected(value.id)
        const newItem = {...item, value: value.id}
        dispatch(FormUpdateItemAsyncAction({item: newItem}))
        .then(
            CheckGQLError({
                "ok": () => {
                    dispatch(MsgFlashAction({title: "Vybrano ok"}))
                },
                "fail": (json) => dispatch(MsgAddAction({title: "Výběr se nepovedl\n"+ JSON.stringify(json)})),
            })
        )
        
    }
    // console.log("StudentItemEdit preif", user)
    if (user) {
        
        return (
            <Row>

                <Col>
                    {/* {JSON.stringify(user)} */}
                    <UserSearch key={user.id} onSelect={onSelect} label="User" user={user} clearOnClose={false}/>
                </Col>
            </Row>
        ) 
    } else {
        return (
            <Row>
                <Col>
                    {/* {JSON.stringify(user)} */}
                    <UserSearch key="undefined" onSelect={onSelect} label="User" clearOnClose={false}/>
                </Col>
            </Row>
        )
    }
}

export const StudentItemRead = ({item}) => {
    const user = useFreshItem({id: item.value}, UserFetchAsyncAction)
    if (user) {
        return (
            <Row>
                <Col md={2}>
                    <b>{item.name} ({item?.type?.name})</b>
                </Col>
                <Col md={10}>
                    <Link tag="user" id={user.id}>{user.name} {user.surname} ({user.email})</Link>
                </Col>
            </Row>
        )    
    }
    else {
        return <MasterItem item={item} />
    }
}

export const StudentItem = ({item, mode}) => {
    // console.log("StudentItem.mode", mode)
    if (mode === "edit") {
        return <StudentItemEdit item={item} />
    } else {
        return <StudentItemRead item={item} />
    }
}