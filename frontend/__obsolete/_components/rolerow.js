import Row from "react-bootstrap/Row";
import Col from "react-bootstrap/Col";

import { TeacherSmall } from 'components/links';

export const RoleRow = (props) => {
    //console.log(JSON.stringify(props))
    return (
        <Row>
            <Col md={4}><b>{props.roletype.name}</b></Col>
            <Col md={8}>
                <TeacherSmall {...props.user}/>
            </Col>
        </Row>
    )
}

