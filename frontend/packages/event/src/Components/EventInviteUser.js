import { UserSearch } from "@uoisfrontend/user"
import { CheckGQLError, MsgAddAction, MsgFlashAction } from "@uoisfrontend/shared";
import { EventInvitationSelect, InvitationTypeSelect } from "./EventInvitationSelect"
import { EventInvitationInsertAsyncAction } from "../Actions/EventInvitationInsertAsyncAction"

import { useState } from "react"
import { useDispatch } from "react-redux"
import Row from "react-bootstrap/Row"
import Col from "react-bootstrap/Col"

export const EventInviteUser = ({event}) => {
    const [invitationtype_id, setInvitationType] = useState(null)
    const dispatch = useDispatch()
    const onUserSelect = (user) => {
        if (invitationtype_id) {
            const isInvited = event?.presences.map(presence => presence.user.id).find(u => u.id === user.id)
            if (isInvited) {}
            else {
                console.log("EventInviteUser", event.id, user.id, invitationtype_id)
                dispatch(EventInvitationInsertAsyncAction(event.id, user.id, invitationtype_id))
                // event_id, user_id, invitation_type_id
                .then(
                    CheckGQLError({
                        "ok": () => dispatch(MsgFlashAction({title: "Pozvání ok"})),
                        "fail": (json) => dispatch(MsgAddAction({title: "Pozvání se nepovedlo\n " + JSON.stringify(json)}))
                    })
                )
            }
        }
    }
    const onInvitationSelect = (id) => {
        setInvitationType(id)
    }

    return (
        <Row>
            <Col>
                <InvitationTypeSelect value={invitationtype_id} onSelect={onInvitationSelect}  /> 
            </Col>
            <Col>
                <UserSearch onSelect={onUserSelect}/>
            </Col>
        </Row>
    )
}