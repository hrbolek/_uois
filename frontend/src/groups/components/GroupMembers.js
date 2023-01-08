import Card from "react-bootstrap/Card";
import Row from "react-bootstrap/Row";
import Col from "react-bootstrap/Col";

import { UserSmall } from "users/components/links"

const Member = (props) => {
    return (
        <Row><Col><UserSmall user={props.user}/></Col></Row>
    )
}

export const GroupMembers = (props) => {
    const { group } = props
    const memberships = group.memberships?.filter(m => m.valid) || []
    return (
        <Card>
            <Card.Header>
                <Card.Title>
                    Members
                </Card.Title>
            </Card.Header>
            <Card.Body>
                {memberships.map(
                    m => <Member key={m.id} user={m.user}/>
                )
                }
            </Card.Body>
        </Card>
    )
}