import All from "@uoisfrontend/shared/src/keyedreducers"
import { Alert, Button } from "react-bootstrap"
import Container from 'react-bootstrap/Container';

import { useDispatch } from "react-redux"
import { useSelector } from "react-redux"
import { Msgs } from "@uoisfrontend/shared/src/msgs"
import Row from "react-bootstrap/Row"
import Col from "react-bootstrap/Col"
import { useState } from "react"
import { ArrowLeftRight, MenuApp } from "react-bootstrap-icons"
export const Menu = ({actions}) => {
    return (
        <></>
    )
}

// export const Msg = ({msg, actions}) => {
//     const dispatch = useDispatch()

//     const onClose = () => 
//         dispatch(All.DeleteItem(msg))
//         // actions.onMessageRemove(msg)
//     return (
//         <Alert variant={msg.variant} onClose={onClose}>
//             <div className="row">
//                 <div className="col">
//                     {msg?.title}
//                 </div>   
//                 <div className="col d-flex justify-content-end">
//                     <Button onClick={onClose} variant="outline-success">
//                         Close
//                     </Button>
//                 </div>
//             </div>
//         </Alert>
//     )
// }

// export const Msgs = ({actions}) => {
//     const msgs = useSelector(state => state.msgs)
//     return (
//         <>
//             {Object.values(msgs).map(
//                 msg => <Msg key={msg.id} msg={msg} actions={actions} />
//             )}
//         </>
//     )
// }

const spinid = "75ad5439-78c4-4172-82d0-ba16be72fbb3"
export const Spinner = () => {
    const items = useSelector(state => state.items)
    const spin = items[spinid] || false

    if (spin === true) {
        return (
            <div style={{position: "relative"}}>
                <div className="" style={{position: "relative", top: "0px", zIndex: "10", width: "100%", height: "100vh"}}>
                    <div className="position-absolute top-50 start-50">
                        <div className="spinner-border text-primary" role="status">
                            <span className="visually-hidden">Loading...</span>
                        </div>
                    </div>
                </div>
            </div>
    )}
}

export const LeftMenu = () => {
    return (
        <Col md={1}>
            <div className="sticky-md-top">
                WTF
            </div>
        </Col>
    )
}

export const Layout = ({children, actions}) => {
    const [visible, setVisible] = useState(false)
    const onClick = () => setVisible(!visible)
    return (
        <Container fluid>
            <Row>
                {visible? <LeftMenu /> : ''}
                <Col>
                    <Menu />
                    <Spinner />
                    <Msgs actions={actions}/>
                    {children}
                </Col>
            </Row>
        </Container>
        
        // <Row>
        //     {visible? <LeftMenu /> : ''}
        //     <Col>
        //         <Menu />
        //         <Spinner />
        //         <Msgs actions={actions}/>
        //         {children}
        //     </Col>
        // </Row>
    
)
}