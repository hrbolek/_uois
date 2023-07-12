import Card from "react-bootstrap/Card"
import Col from "react-bootstrap/Col"
import Row from "react-bootstrap/Row"

import { PencilSquare, PersonFill, Receipt } from "react-bootstrap-icons"
import { Demo, Link } from "@uoisfrontend/shared"

const Question = ({question}) => {
    return (
        <span className="btn btn-outline-success">{question.name}</span>
    )
}

const OneSurvey = ({answers}) => {
    const answer = answers[0] || {}
    const survey = answer?.question?.survey || {}
    return (
        <Card>
            <Card.Header>
                Anketa <span className="btn btn-outline-success">{survey.name}</span>
            </Card.Header>
            <Card.Body>
                {answers.map(answer => <><Question question={answer?.question}/><br />{answer?.value}<br />{JSON.stringify(answer)}<br /><br /></>)}
            </Card.Body>
        </Card>
        
    )
}

export const SurveyUserCard = ({user}) => {
    const answers = user?.answers || []
    const surveys = answers.map(answer => [answer?.question?.survey, answer])
    const reducedsurveys = surveys.reduce((acc, [survey, answer]) => {
        const value = acc[survey.id] || []
        value.push(answer)
        acc[survey.id] = value
        return acc
    }, {})
    return (
        <Card>
            <Card.Header>
                <Row>
                    <Col>
                        <Receipt /> 
                    </Col>
                    <Col>
                        <Link id={user.id} tag="user"><PersonFill /> {user.name} {user.surname} </Link>
                    </Col>
                    <Col>
                        
                    </Col>
                    <Col>
                        <div className="d-flex justify-content-end">
                            <Link id={user.id} tag="user"><PersonFill /> </Link>
                        </div>
                    </Col>
                </Row>

            </Card.Header>
            <Card.Body>
               {Object.entries(reducedsurveys).map(
                    ([survey, answers]) => <><OneSurvey answers={answers} /></>
               )} 
            </Card.Body>
            <Card.Body>
                {JSON.stringify(user?.answers)} <br /><br />
                {JSON.stringify(reducedsurveys)}
            </Card.Body>
        </Card>
    )
}