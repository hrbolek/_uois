import Row from "react-bootstrap/Row"
import Col from "react-bootstrap/Col"
import { CheckGQLError, Link, MsgAddAction, MsgFlashAction, useFreshItem } from "@uoisfrontend/shared"
import { useState } from "react"
import { useDispatch } from "react-redux"
import { FormUpdateItemAsyncAction } from "../../Actions/FormUpdateItemAsyncAction"
// import { UserFetchAsyncAction } from "@uoisfrontend/user/UserFetchAsyncAction"

export const MultiLineItemEdit = ({item}) => {
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

    return (
        <Row>
            <Col>
                <div class="form-floating">
                    <textarea style={{height: "150px"}} class="form-control" placeholder="Leave a comment here" id={item.id + "floatingTextarea"}>{item.value}</textarea>
                    <label for={item.id + "floatingTextarea"}>{item.name}</label>
                </div>
            </Col>
        </Row>
    ) 
}

export const MultiLineItemRead = ({item}) => {
    return (
        <Row>
            <Col md={2}>
                <b>{item.name} ({item?.type?.name})</b>
            </Col>
            <Col md={10}>
                {item?.value}
            </Col>
        </Row>
    )    
}

export const MultiLineItem = ({item, mode}) => {
    // console.log("MultiLineItem.mode", mode)
    if (mode === "edit") {
        return <MultiLineItemEdit item={item} />
    } else {
        return <MultiLineItemRead item={item} />
    }
}