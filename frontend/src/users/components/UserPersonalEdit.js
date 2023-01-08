import Card from "react-bootstrap/Card";
import Row from "react-bootstrap/Row";
import Col from "react-bootstrap/Col";

import { useState, useEffect } from "react";

import { UserSmall } from 'users/components/links';

export const EditableTextAttribute = (props) => {
    const { attributeName, placeholder } = props
    const [attributeValue, setAttributeValue] = useState(props[attributeName])
    
    useEffect( // a little hack
        () => {
            setAttributeValue(props[attributeName])
        }, [props, attributeName]
    )

    const localChangeAtribute = (e) => {
        const newAttributeValue = e.target.value
        setAttributeValue(newAttributeValue)
        if (props.onChange) {
            props.onChange(attributeName, newAttributeValue)
            //console.log(attributeName, newAttributeValue)
        }
    }
    return (
        <input type="text" className="form-control" placeholder={placeholder} aria-label={placeholder} value={attributeValue} onChange={localChangeAtribute}/>
    )
}

export const UserPersonalEdit = (props) => {
    const { user } = props
    const onChange = (name, value) => {
        const userRow = {'id': user.id, 'name': user.name, 'surname': user.surname, 'email': user.email}
        userRow[name] = value
        if (props.actions) {
            //console.log(teacherRow)
            props.actions.updateUser(userRow)
        }
    }
    return (
        <Card>
            <Card.Header>
                <Card.Title>
                    <UserSmall user={user} />
                </Card.Title>
            </Card.Header>
            <Card.Body>
                <Row>
                    <Col><b>Jméno</b></Col><Col><EditableTextAttribute {...user} attributeName={"name"} placeholder={"zadejte jméno"} onChange={onChange} /></Col>
                </Row>
                <Row>
                    <Col><b>Příjmení</b></Col><Col><EditableTextAttribute {...user} attributeName={"surname"} placeholder={"zadejte příjmení"} onChange={onChange} /></Col>
                </Row>
                <Row>
                    <Col><b>Email</b></Col><Col><EditableTextAttribute {...user} attributeName={"email"} placeholder={"zadejte email"} onChange={onChange} /></Col>
                </Row>
            </Card.Body>
        </Card>
    )
}