import Card from "react-bootstrap/Card";
import Row from "react-bootstrap/Row";
import Col from "react-bootstrap/Col";

import { UserSmall } from 'users/components/links';
import { ExpandableButton } from 'generals/components/ExpandableButton'

export const TeacherGrantProgramsActual = (props) => {
    return (
        <Card>
            <Card.Header>
                <Card.Title>
                    Garant - Platné programy 
                </Card.Title>
            </Card.Header>
            <Card.Body>

            </Card.Body>
        </Card>
    )
}

export const TeacherGrantProgramsPast = (props) => {
    return (
        <Card>
            <Card.Header>
                <Card.Title>
                    Garant - Neplatné programy
                </Card.Title>
            </Card.Header>
            <Card.Body>

            </Card.Body>
        </Card>
    )
}



const garanceB = [
    {'name': 'Ekonomika obrany státu - EKOS', 'id': 62904, 'teachers': [
        {'role': 'Garant', 'teacher': {'name': 'Jakub', 'surname': 'Odehnal', 'id': 8776}},
        {'role': 'Zastupce garanta', 'teacher': {'name': 'Aleš', 'surname': 'Olejníček', 'id': 5509}},
        {'role': 'Vyučující', 'teacher': {'name': 'Vladan', 'surname': 'Holcner ', 'id': 1232}},             
        {'role': 'Vyučující', 'teacher': {'name': 'Miroslav', 'surname': 'Krč', 'id': 9306}},
        {'role': 'Vyučující', 'teacher': {'name': 'Jiří', 'surname': 'Neubauer', 'id': 5485}},
        {'role': 'Vyučující', 'teacher': {'name': 'Aleš', 'surname': 'Olejníček', 'id': 8776}},
        {'role': 'Vyučující', 'teacher': {'name': 'Aleš', 'surname': 'Olejníček', 'id': 5509}},
        {'role': 'Vyučující', 'teacher': {'name': 'Josef', 'surname': 'Procházka', 'id': 1152}},
    ]},
    {'name': 'Řízení obranných zdrojů - ROZ', 'id': 1054, 'teachers': [
        {'role': 'Garant', 'teacher': {'name': 'Jakub', 'surname': 'Odehnal', 'id': 8776}},
        {'role': 'Zastupce garanta', 'teacher': {'name': 'Aleš', 'surname': 'Olejníček', 'id': 5509}},
        {'role': 'Vyučující', 'teacher': {'name': 'Vladan', 'surname': 'Holcner ', 'id': 1232}},             
        {'role': 'Vyučující', 'teacher': {'name': 'Miroslav', 'surname': 'Krč', 'id': 9306}},
        {'role': 'Vyučující', 'teacher': {'name': 'Jiří', 'surname': 'Neubauer', 'id': 5485}},
        {'role': 'Vyučující', 'teacher': {'name': 'Aleš', 'surname': 'Olejníček', 'id': 8776}},
        {'role': 'Vyučující', 'teacher': {'name': 'Aleš', 'surname': 'Olejníček', 'id': 5509}},
        {'role': 'Vyučující', 'teacher': {'name': 'Josef', 'surname': 'Procházka', 'id': 1152}},
    ]},
    {'name': 'Základy ekonomických vztahů - ZEV', 'id': 316, 'teachers': [
        {'role': 'Garant', 'teacher': {'name': 'Jakub', 'surname': 'Odehnal', 'id': 8776}},
        {'role': 'Zastupce garanta', 'teacher': {'name': 'Aleš', 'surname': 'Olejníček', 'id': 5509}},
        {'role': 'Vyučující', 'teacher': {'name': 'Vladan', 'surname': 'Holcner ', 'id': 1232}},             
        {'role': 'Vyučující', 'teacher': {'name': 'Miroslav', 'surname': 'Krč', 'id': 9306}},
        {'role': 'Vyučující', 'teacher': {'name': 'Jiří', 'surname': 'Neubauer', 'id': 5485}},
        {'role': 'Vyučující', 'teacher': {'name': 'Aleš', 'surname': 'Olejníček', 'id': 8776}},
        {'role': 'Vyučující', 'teacher': {'name': 'Aleš', 'surname': 'Olejníček', 'id': 5509}},
        {'role': 'Vyučující', 'teacher': {'name': 'Josef', 'surname': 'Procházka', 'id': 1152}},
    ]}
  ]

export const GrantRow = (props) => {
    return (
        <tr>
            <td>TOS</td>
            <td>{props.name}</td>
            <td>
                <ExpandableButton className="btn btn-sm btn-outline-success">Studentské hodnocení</ExpandableButton>
                <ExpandableButton className="btn btn-sm btn-danger">Naplánovat PSP</ExpandableButton>
            </td>
        </tr>
    )
}

export const TeacherGrantSubjectsActual = (props) => {
    return (
        <Card>
            <Card.Header>
                <Card.Title>
                    Garant - Platné předměty
                </Card.Title>
            </Card.Header>
            <Card.Body>
                <table className="table table-bordered table-striped">
                    <thead>
                        <tr>
                            <td className="w-25">Program</td>
                            <td className="w-50">Předmět</td>
                            <td className="w-25">Nástroje</td>
                        </tr>
                    </thead>
                    <tbody>
                        {
                            garanceB.map( predmet => <GrantRow {...predmet}/>)
                        }
                    </tbody>
                </table>
            </Card.Body>
        </Card>
    )
}

export const TeacherGrantSubjectsPast = (props) => {
    return (
        <Card>
            <Card.Header>
                <Card.Title>
                    Garant - Neplatné předměty
                </Card.Title>
            </Card.Header>
            <Card.Body>

            </Card.Body>
        </Card>
    )
}

export const TeacherGrant = (props) => {
    return (
        <Card>
            <Card.Header>
                <Card.Title>
                    Garant <UserSmall user={props.user} />
                </Card.Title>
            </Card.Header>
            <Card.Body>
                <Row>
                    <Col md={6}>
                        <TeacherGrantProgramsActual user={props.user} />
                    </Col>
                    <Col md={6}>
                        <TeacherGrantSubjectsActual user={props.user} />
                    </Col>
                </Row>
                <Row>
                    <Col md={6}>
                        <TeacherGrantProgramsPast user={props.user} />
                    </Col>
                    <Col md={6}>
                        <TeacherGrantSubjectsPast user={props.user} />
                    </Col>
                </Row>
            </Card.Body>
        </Card>
    )
}