import Row from "react-bootstrap/Row";
import Col from "react-bootstrap/Col";

import { TeacherSmall } from 'usersgroups/components/links';

export const RoleRow = (props) => {
    //console.log(JSON.stringify(props))
    const { role } = props
    return (
        <Row>
            <Col md={4}><b>{role.roletype.name}</b></Col>
            <Col md={8}>
                <TeacherSmall user={role.user}/>
            </Col>
        </Row>
    )
}

