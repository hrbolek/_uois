import Row from "react-bootstrap/Row"
import Col from "react-bootstrap/Col"
import { GroupNameEditable } from "./GroupNameEditable"
import { GroupTypeEditable } from "./GroupTypeEditable"

export const GroupAttributesEditable = ({group}) => {
    return (
        <>
            <Row>
                {/* <Col md={2}>
                    Název
                </Col> */}
                <Col>
                    <GroupNameEditable group={group} />
                </Col>
            </Row>
            <Row>
                {/* <Col md={2}>
                    Typ
                </Col> */}
                <Col>
                    <GroupTypeEditable group={group} />
                </Col>
            </Row>
        </>
    )
}