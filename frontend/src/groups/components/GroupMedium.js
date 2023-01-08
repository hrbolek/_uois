import Card from "react-bootstrap/Card";
import Row from "react-bootstrap/Row";
import Col from "react-bootstrap/Col";

import { RowRoles } from 'groups/components/GroupRoles'
import { GroupSmall } from 'groups/components/links'

export const GroupMedium = (props) => {
    return (
        <Card>
            <Card.Header>
                <Card.Title>
                    <GroupSmall group={props.group} />
                </Card.Title>
            </Card.Header>
            <Card.Body>
                <RowRoles {...props} /> <br />
            </Card.Body>
        </Card>
    )
}