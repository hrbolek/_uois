import Card from "react-bootstrap/Card";
import Row from "react-bootstrap/Row";
import Col from "react-bootstrap/Col";

import { RolesCard } from 'usersgroups/components/RolesCard';
import { FacultySmall, UniversitySmall } from 'usersgroups/components/links'

import { GroupMembers } from 'usersgroups/components/GroupMembers';

export const DepartmentLarge = (props) => {
    return (
        <Card>
            <Card.Header>
                <Card.Title>
                    <FacultySmall {...props.mastergroup}/> / {props.name}
                </Card.Title>
            </Card.Header>
            <Card.Body>
                <Row>
                    <Col md={3}>
                        <RolesCard {...props}/>
                    </Col>
                    <Col md={3}>
                        <GroupMembers {...props}/>
                    </Col>
                </Row>
            </Card.Body>
            <Card.Footer>
                {JSON.stringify(props)}
            </Card.Footer>
        </Card>
    )
}