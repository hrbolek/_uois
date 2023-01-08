import Card from "react-bootstrap/Card";
import Row from "react-bootstrap/Row";
import Col from "react-bootstrap/Col";

import { UserSmall } from "users/components/links"

const Role = (props) => {
    const { roletype, user } = props
    return (
        <Row>
            <Col><b>{roletype.name}</b></Col>
            <Col><UserSmall user={user}/></Col>
        </Row>
    )
}

export const RowRoles = (props) => {
    const { group } = props
    const roles = group.roles
    return (
        <>
        {roles?.map(
            (r) => <Role key={r.id} {...r} />
        )}
        </>
    )
}

export const GroupRoles = (props) => {
    return (
        <Card>
            <Card.Header>
                <Card.Title>
                    Vedení
                </Card.Title>
            </Card.Header>
            <Card.Body>
                <RowRoles {...props} />
            </Card.Body>
        </Card>
    )
}