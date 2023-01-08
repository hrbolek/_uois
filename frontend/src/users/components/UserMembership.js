import Card from "react-bootstrap/Card";
import Row from "react-bootstrap/Row";
import Col from "react-bootstrap/Col";

import { UserSmall } from 'users/components/links';
import { GroupSmall } from 'groups/components/links';

const UserMembershipRow = (props) => {
    const { group } = props
    const { grouptype } = group
    return (
        <>
        <Row>
            <Col><b>{grouptype.name}</b></Col><Col><GroupSmall group={group} /></Col>
        </Row>
        </>
    )
}

export const UserMembership = (props) => {
    const { user } = props
    const validmembership = user.membership.filter(m => m.valid)
    return (
        <Card>
            <Card.Header>
                <Card.Title>
                    <UserSmall user={user} />
                </Card.Title>
            </Card.Header>
            <Card.Body>
                {validmembership.map(
                    (m, index) => <UserMembershipRow key={index} group={m.group} />
                )}
            </Card.Body>
        </Card>
    )
}