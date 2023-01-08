import { useState } from "react"
import Card from "react-bootstrap/Card";
import Row from "react-bootstrap/Row";
import Col from "react-bootstrap/Col";

import { UserSmall } from 'users/components/links';
import { SheetA4TimeTable } from 'events/components/SheetA4TimeTable'
import { WeekTimeTable } from 'events/components/WeekTimeTable'


const TodayDate = () => {
    const today = new Date();
    today.setHours(0)
    today.setMinutes(0)
    today.setSeconds(0)
    return today
}

const PrevMonday = () => {

}

export const TeacherTimeTable = (props) => {
    const { user } = props
    const [today, setToday] = useState(TodayDate())

    const events = [
        {}
    ]


    return (
        <Card>
            <Card.Header>
                <Card.Title>
                    Rozvrh <UserSmall user={user} />  
                </Card.Title>
            </Card.Header>
            <Card.Body>
                <Row>
                    <Col md={12}>
                        <WeekTimeTable />
                    </Col>
                </Row>
            </Card.Body>
        </Card>
    )
}