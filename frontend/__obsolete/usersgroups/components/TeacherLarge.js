import Card from "react-bootstrap/Card";
import Row from "react-bootstrap/Row";
import Col from "react-bootstrap/Col";

import { useEffect, useState } from 'react'
import { userUpdateQuery } from 'usersgroups/queries/user'
import { CreateDelayer } from 'usersgroups/reducers/usermain'

import { TeacherSmall } from 'usersgroups/components/links'

export const TeacherMembership = (props) => {
    const { user } = props
    const { membership } = user
    const validMemberships = membership.filter( m => m.valid)
    //console.log('TeacherMembership')
    //console.log(JSON.stringify(membership))
    return (
            <>
            {validMemberships.map((item, index) => {
                
                return (
                    <Row key={item.group.id}>
                        <Col><b>{item.group?.grouptype?.name}</b></Col>
                        <Col>{item.group.name}</Col>
                    </Row>
                )
            }
            )}
            </>
    )
}

export const TeacherRoles = (props) => {
    const { user } = props
    const { roles } = user
    //console.log('TeacherRoles')
    //console.log(JSON.stringify(TeacherRoles))
    return (
            <>
            {roles.map((item, index) => {
                console.log(JSON.stringify(item))
                return (
                    <Row key={item.id}>
                        <Col><b>{item.roletype?.name}</b></Col>
                        <Col>{item.group?.name}</Col>
                    </Row>
                )
            }
            )}
            </>
    )
}

export function TeacherMedium(props) {
    return (
        <Card>
            <Card.Header>
                <Card.Title>
                    <TeacherSmall user={props.user}/>
                </Card.Title>
            </Card.Header>
            <Card.Body>
                <Row>
                    <b>Členství</b>
                    <hr />
                </Row>
                <Row>
                    <TeacherMembership user={props.user}/>
                </Row>
            </Card.Body>
            <Card.Body>
                <Row>
                    <b>Role</b>
                    <hr />
                </Row>
                <Row>
                    <TeacherRoles user={props.user}/>
                </Row>
            </Card.Body>
        </Card>
    )
}

const ApiDelayer = CreateDelayer()

export const TeacherName = (props) => {
    const [name, setName] = useState(props.name)

    const changeName = (e) => {
        const newName = e.target.value
        setName(newName)

        ApiDelayer(() => userUpdateQuery({id: props.id, name: newName}))
    }
    return (
        <input type="text" className="form-control" placeholder="Username" aria-label="Username"  value={name} onChange={changeName}/>
    )
}

export const EditableTextAttribute = (props) => {
    const { attributeName, placeholder } = props
    const [attributeValue, setAttributeValue] = useState(props[attributeName])
    
    useEffect( // a little hack
        () => {
            setAttributeValue(props[attributeName])
        }, [props[attributeName]]
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

export const TeacherPersonalsEditable = (props) => {
    const { user } = props
    const onChange = (name, value) => {
        const teacherRow = {'id': user.id, 'name': user.name, 'surname': user.surname, 'email': user.email}
        teacherRow[name] = value
        if (props.actions) {
            //console.log(teacherRow)
            props.actions.updateUser(teacherRow)
        }
    }
    return (
        <Card>
            <Card.Header>
                <Card.Title>
                    Osobní údaje
                </Card.Title>
            </Card.Header>
            <Card.Body>
                <Row>
                    <Col md={6}>
                        <Row>
                            <Col><b>Jméno</b></Col><Col><EditableTextAttribute {...user} placeholder="Jméno" attributeName="name" onChange={onChange}/></Col>
                        </Row>
                        <Row>
                            <Col><b>Příjmení</b></Col><Col><EditableTextAttribute {...user} placeholder="Jméno" attributeName="surname" onChange={onChange}/></Col>
                        </Row>
                        <Row>
                            <Col><b>Email</b></Col><Col><EditableTextAttribute {...user} placeholder="Jméno" attributeName="email" onChange={onChange}/></Col>
                        </Row>

                    </Col>
                    <Col md={6}>
                        <Row>
                            <b>Členství</b>
                            <hr />
                        </Row>
                        <Row>
                            <TeacherMembership user={user}/>
                        </Row>                        
                        <Row>
                            <b>Role</b>
                            <hr />
                        </Row>
                        <Row>
                            <TeacherRoles user={user}/>
                        </Row>
                    </Col>
                </Row>
            </Card.Body>
        </Card>
    )
}

export const TeacherPersonals = (props) => {
    const { user } = props
    return (
        <Card>
            <Card.Header>
                <Card.Title>
                    Osobní údaje
                </Card.Title>
            </Card.Header>
            <Card.Body>
                <Row>
                    <Col md={6}>
                        <Row>
                            <Col><b>Jméno</b></Col><Col>{user.name}</Col>
                        </Row>
                        <Row>
                            <Col><b>Příjmení</b></Col><Col>{user.surname}</Col>
                        </Row>
                        <Row>
                            <Col><b>Email</b></Col><Col>{user.email}</Col>
                        </Row>

                    </Col>
                    <Col md={6}>
                        <Row>
                            <b>Členství</b>
                            <hr />
                        </Row>
                        <Row>
                            <TeacherMembership user={user}/>
                        </Row>                        
                        <Row>
                            <b>Role</b>
                            <hr />
                        </Row>
                        <Row>
                            <TeacherRoles user={user}/>
                        </Row>
                    </Col>
                </Row>
            </Card.Body>
            <Card.Body>
                {JSON.stringify(Object.keys(props.actions))}
            </Card.Body>
        </Card>
    )
}
export function TeacherLarge(props) { 
    return (
        

        <Card>
            <Card.Header>
                <Card.Title>Title</Card.Title>
            </Card.Header>
            <Card.Body>
                <TeacherMedium user={props.user} />
            </Card.Body>
        </Card>
    )
}