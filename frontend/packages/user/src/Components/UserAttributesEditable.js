import { UserEmailEditable } from "./UserEmailEditable"
import { UserNameEditable } from "./UserNameEditable"
import { UserSurnameEditable } from "./UserSurnameEditable"
import Row from "react-bootstrap/Row"
import Col from "react-bootstrap/Col"

/**
 * 
 * @param {Object} props.user an user whos attributes will be shown and enabled to edit
 *  
 * @returns JSX.Element
 */
export const UserAttributesEditable = ({user}) => {
    return (
        <>
            <Row>
                <Col md={2}>
                    Jméno
                </Col>
                <Col>
                    <UserNameEditable user={user} /> 
                </Col>
            </Row>
            <Row>
                <Col md={2}>
                    Příjmení
                </Col>
                <Col>
                    <UserSurnameEditable user={user} />
                </Col>
            </Row>
            <Row>
                <Col md={2}>
                    email
                </Col>
                <Col>
                    <UserEmailEditable user={user} />
                </Col>
            </Row>            
        </>
    )
}