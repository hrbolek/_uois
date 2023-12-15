import { createSlice } from '@reduxjs/toolkit';
import { CreateItem, DeleteItem } from './keyedreducers';
import Alert from 'react-bootstrap/Alert';
import Button from 'react-bootstrap/Button';
import Toast from 'react-bootstrap/Toast';
import ToastContainer from 'react-bootstrap/ToastContainer';
import { useDispatch, useSelector } from 'react-redux';
import { v1 as uuid } from 'uuid';

/**
* Kompletni rez budocim store.
* Obsluhuje skupiny
*/
const MsgSlice = createSlice({
   name: 'msgs',
   initialState: {},
   reducers: {
       msg_add: CreateItem,
       msg_delete: DeleteItem
   }
})

export const MsgReducer = MsgSlice.reducer
export const MsgActions = MsgSlice.actions

export const Msg_ = ({msg}) => {
    const dispatch = useDispatch()
    const onClose = () => {
        dispatch(MsgActions.msg_delete(msg))
    }
    const buttonStyle = msg?.variant ? ("outline-" + msg.variant) : "outline-success"
    return (
        <Alert variant={msg.variant} onClose={onClose}>
            <div className="row">
                <div className="col">
                    {msg?.title}
                </div>   
                <div className="col d-flex justify-content-end">
                    <Button onClick={onClose} variant={buttonStyle}>
                        Close
                    </Button>
                </div>
            </div>
        </Alert>
    )
}

export const Msg = ({msg}) => {
    const dispatch = useDispatch()
    const onClose = () => {
        dispatch(MsgActions.msg_delete(msg))
    }
    const buttonStyle = msg?.variant ? ("outline-" + msg.variant) : "outline-success"
    return (
        <Toast bg={msg.variant} onClose={onClose}>
            <Toast.Header>
                {/* <div className="col d-flex justify-content-end">
                    <Button onClick={onClose} variant={buttonStyle}>
                        Close
                    </Button>
                </div> */}
            </Toast.Header>
            <Toast.Body>
                {msg?.title}
            </Toast.Body>
        </Toast>
    )
}

export const Msgs_ = () => {
    const msgs = useSelector(state => state.msgs)
    return (
        <>
            {Object.values(msgs).map(
                msg => <Msg key={msg.id} msg={msg} />
            )}
        </>
    )
}

export const Msgs = () => {
    const msgs = useSelector(state => state.msgs)
    return (
        <ToastContainer position='bottom-end'>
            {Object.values(msgs).map(
                msg => <Msg key={msg.id} msg={msg} />
            )}
        </ToastContainer>
    )
}

export const MsgFlashAction = ({title, delay = 5000, variant = "success"}) => (dispatch, getState) => {
    const msgWithId = {id: uuid(), variant: variant, title: title}

    setTimeout(
        () => dispatch(MsgActions.msg_delete(msgWithId)), delay
    )
    return dispatch(MsgActions.msg_add(msgWithId))
}

export const MsgAddAction = ({title, variant = "danger"}) => (dispatch, getState) => {
    const msgWithId = {id: uuid(), variant: variant, title: title}

    return dispatch(MsgActions.msg_add(msgWithId))
}

/**
 * @param {function} reactions.errors function to be called when gql endpoint returns json.errors 
 * @param {function} reactions.fail function to be called when mutation returns json.data.result.msg has no value "ok" and reactions[msg] not present
 * @param {function} reactions.ok function to be called when mutation returns json.data.result or json.data.result.msg is has value "ok"
 */
export const CheckGQLError = (reactions) => (json) => {
    
    console.log("CheckGQLError call")
    const errors = json?.errors
    if (errors) {
        const reaction = reactions?.errors || reactions?.error || reactions["fail"]
        reaction(json)
    } else {
        const msg = json?.data?.result?.msg
        if (msg) {
            const reaction = reactions[msg] || reactions["fail"]
            // const successVariant = "success"
            // const dangerVariant = "danger"
            // const defaultVariant = reaction === "ok" ? successVariant : dangerVariant
            // const variant = reaction?.variant || defaultVariant
            // const label = reaction || ("Změna " + msg)
            // if (variant === successVariant) {
                
            // } else {
            //     variant()
            // }
            if (reaction) {
                reaction(json)
            } else {
                console.warn("no proper reaction found", json)
            }
            
        } else {
            const jsonresult = json?.data?.result
            if (jsonresult) {
                const reaction = reactions["ok"]
                if (reaction) {
                    reaction(json)
                } else {
                    console.error("ok reaction missing")
                }
                    
            } else {
                const reaction = reactions?.errors || reactions?.error || reactions?.fail
                if (reaction) {
                    reaction(`Data nenalezena. ${JSON.stringify(json)}  Server nenašel položku v databázi. Položka neexistuje.`)
                }
                
                console.warn("no proper reaction found", json)
            }
            
        }
    }
    return json
}

// fetch().then(
//     CheckMutationMsg({ok: () => MsgFlashAction(), fail: "Chyba"})()
// )