import Card from "react-bootstrap/Card";
import Row from "react-bootstrap/Row";
import Col from "react-bootstrap/Col";

import { UserSmall } from 'users/components/links';

import { ExpandableButton } from 'generals/components/ExpandableButton'

const GroupRow = (props) => {
    return (
        <tr>
            <td>{props.name}</td>
            <td>{props.subj}</td>
            <td>17</td>
            <td>7</td>
            <td>.</td>
            <td>.</td>
            <td>
                <ExpandableButton className="btn btn-sm btn-outline-success">Detail</ExpandableButton>
                <ExpandableButton className="btn btn-sm btn-outline-success">Třídní kniha</ExpandableButton>
                <ExpandableButton className="btn btn-sm btn-outline-success">Plán studia</ExpandableButton>
                <ExpandableButton className="btn btn-sm btn-outline-success">Akreditace</ExpandableButton>
                <ExpandableButton className="btn btn-sm btn-outline-success">Zápis</ExpandableButton>
            </td>
        </tr>
    )
}

const groups = [
    {'id': '46487979', 'name': '23-5KB', 'subj': 'Analýza informačních zdrojů' },
    {'id': '46487979', 'name': '23-5KB', 'subj': 'Kybernetická bezpečnost' },
]

export const TeacherStudyGroups = (props) => {
    const { user } = props
    return (
        <Card>
            <Card.Header>
                <Card.Title>
                    Vyučované skupiny <UserSmall user= {user} />
                </Card.Title>
            </Card.Header>
            <Card.Body>
                <Row>
                    <Col md={12}>
                        <table className="table table-striped table-bordered">
                            <thead>
                                <tr>
                                    <td className="w-25">#</td>
                                    <td className="w-25">Předmět</td>
                                    <td className="w-10">VZP</td>
                                    <td className="w-10">C</td>
                                    <td className="w-10">.</td>
                                    <td className="w-10">.</td>
                                    <td className="w-25">Nástroje</td>
                                </tr>
                            </thead>
                            <tbody>
                                {groups.map( g => <GroupRow {...g}/>)}
                            </tbody>
                        </table>
                    </Col>
                </Row>
            </Card.Body>
        </Card>
    )
}