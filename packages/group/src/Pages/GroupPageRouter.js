import Row from 'react-bootstrap/Row'
import Col from 'react-bootstrap/Col'
import { Link, json, useLoaderData, useRouteLoaderData } from 'react-router-dom'
import { Card } from 'react-bootstrap'
import { GroupRoles } from '../Components'

const LocalLink = ({group}) => {
    return (
        <Card>
            <Card.Header>
                <Link to={"../" + group.grouptype.nameEn + "/" + group.id}>{group.name}</Link>
            </Card.Header>
            <Card.Body>
                <GroupRoles group={group} onlyValid={true} />
            </Card.Body>
        </Card>
    )
}

export const GroupPageRouter = ({reference, children}) => {
    // const group = useLoaderData()
    const group = useRouteLoaderData(reference)
    return (
        <Row>
            <Col md={2}>
                <Card>
                    <Card.Header>{group?.name}</Card.Header>
                    <Card.Body>
                        <Row>
                        {group?.subgroups?.map(
                            g => <Col key={g.id} md={3}><LocalLink group={g} /></Col>
                        )}
                        </Row>
                    </Card.Body>
                    <Card.Footer>
                        {JSON.stringify(group)}
                    </Card.Footer>
                </Card>
                
                
                </Col>
            <Col md={10}>{children}</Col>
        </Row>
    )
}