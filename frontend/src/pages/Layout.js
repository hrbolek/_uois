import { Alert, Button } from "react-bootstrap"
import { useSelector } from "react-redux"

export const Menu = ({actions}) => {
    return (
        <></>
    )
}

export const Msg = ({msg, actions}) => {
    const onClose = () => 
        actions.onMessageRemove(msg)
    return (
        <Alert variant={msg.variant} onClose={onClose}>
            <div className="row">
                <div className="col">
                    {msg?.title}
                </div>   
                <div className="col d-flex justify-content-end">
                    <Button onClick={onClose} variant="outline-success">
                        Close
                    </Button>
                </div>
            </div>
        </Alert>
    )
}

export const Msgs = ({actions}) => {
    const msgs = useSelector(state => state.msgs)
    return (
        <>
            {Object.values(msgs).map(
                msg => <Msg key={msg.id} msg={msg} actions={actions} />
            )}
        </>
    )
}

export const Layout = ({children, actions}) => {

    return (<div>
        <Menu />
        <Msgs actions={actions}/>
        {children}
    </div>)
}