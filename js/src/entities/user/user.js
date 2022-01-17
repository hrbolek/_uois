import {
    Link,
    useParams
  } from "react-router-dom";
import { useEffect, useState } from "react";
import Row from 'react-bootstrap/Row';
import Col from 'react-bootstrap/Col';
import Card from 'react-bootstrap/Card';
import CardGroup from 'react-bootstrap/CardGroup';
import Table from 'react-bootstrap/Table';

import { useQueryGQL, LoadingError, Loading } from '../index';
import { root, rootGQL } from '../config';
import { GroupModelTable, GroupModelSmall } from '../group/group'
import { StudyPlanModelFetching, StudyPlanModelMediumForUser } from '../studyplan/studyplan'

/*
 * @param id holds value for unique entity identification
 * @return Future with response from gQL server
 */
export const QueryUserModelByidLarge = (id) => 
    fetch(rootGQL, {
        method: 'POST', // *GET, POST, PUT, DELETE, etc.
        headers: {
            'Content-Type': 'application/json',
        },
        cache: 'no-cache', // *default, no-cache, reload, force-cache, only-if-cached
        redirect: 'follow', // manual, *follow, error
        body: JSON.stringify({"query": 
            `
            query {
                usersById(id: "${id}") {

                    id
                    name
                    surname
                    email
                    lastchange
                    externalId
                    UCO
                    VaVId

                    eventusermodels {
                        eventId
                    }
                    programusermodels {
                        programId
                        roletypeId
                    }
                    usergroupmodels {
                        id
                        groupmodel {
                          name
                          grouptypeId
                          id
                          UIC
                        }
                    }
                    rolemodels {
                        id
                        name
                        lastchange
                        roletypeId
                        userId
                        groupId
                    }
                    subjectusermodels {
                        subjectId
                        roletypeId
                    }
                    studyplanitemteachermodels {
                        id
                        studyplanitemId
                        studyplanitemmodel {
                            studyplanId
                          }
                      }
                    subjecttopicusermodels {
                        id
                        subjecttopicId
                        userId
                        roletypeId
                    }
                }
            }
            `        
        }) // body data type must match "Content-Type" header
    });    


/*
 * @param id holds value for unique entity identification
 * @return Future with response from gQL server
 */
export const QueryUserModelByidRozvrh = (id) => 
    fetch(rootGQL, {
        method: 'POST', // *GET, POST, PUT, DELETE, etc.
        headers: {
            'Content-Type': 'application/json',
        },
        cache: 'no-cache', // *default, no-cache, reload, force-cache, only-if-cached
        redirect: 'follow', // manual, *follow, error
        body: JSON.stringify({"query": 
            `
            query {
                usersById(id: "${id}") {

                    id
                    name
                    surname
                    email
                    lastchange
                    externalId
                    UCO
                    VaVId

                    eventusermodels {
                        id
                        userId
                        eventId
                        eventmodel {
                            id
                            externalId
                            start
                            end
                            eventgroupmodels {
                                groupmodel {
                                id
                                name
                                }
                            }
                        }
                    }
                }
            }
            `        
        }) // body data type must match "Content-Type" header
    });    

/*
 * @param id holds value for unique entity identification
 * @return Future with response from gQL server
 */
export const QueryUserModelByidMedium = (id) => 
    fetch(rootGQL, {
        method: 'POST', // *GET, POST, PUT, DELETE, etc.
        headers: {
            'Content-Type': 'application/json',
        },
        cache: 'no-cache', // *default, no-cache, reload, force-cache, only-if-cached
        redirect: 'follow', // manual, *follow, error
        body: JSON.stringify({"query": 
            `
            query {
                usersById(id: "${id}") {
                    id
                    name
                    surname
                    email
                    lastchange
                    externalId
                    UCO
                    VaVId
                }
            }
            `        
        }) // body data type must match "Content-Type" header
    });    

const entityRoot = root + '/users';

/*
 * @param props.id unique identification
 * @param props.name visual representation of item
 * @param props.label visual representation of item
 * @param props.children embeded items
 * @return 
 */
export const UserModelSmall = (props) =>  {
    if (props.name) {
        return (
            <Link to={entityRoot + `/${props.id}`}>🧍 {props.name} {props.surname} {props.children}</Link>
        )
    } else if (props.label) {
        return (
            <Link to={entityRoot + `/${props.id}`}>🧍 {props.label}{props.children}</Link>
        )
    } else {
        return (
            <Link to={entityRoot + `/${props.id}`}>🧍 {props.id}{props.children}</Link>
        )
    } 
}

/*
 * @param props holds all data needed for proper rendering
 * @return 
 */
export const UserModelMedium = (props) =>  {
    return (
        <Card>
            <Card.Header className='bg-success bg-gradient text-white'>
                <Card.Title>
                    { props.name } { props.surname } ({ props. UCO }) 
                </Card.Title>
            </Card.Header>
            <Card.Body>
                <ul class="list-group">
                    <li class="list-group-item">id : { props.id }</li>
                    <li class="list-group-item">name : { props.name }</li>
                    <li class="list-group-item">surname : { props.surname }</li>
                    <li class="list-group-item">email : { props.email }</li>
                    <li class="list-group-item">lastchange : { props.lastchange }</li>
                    <li class="list-group-item">externalId : { props.externalId }</li>
                    <li class="list-group-item">UCO : { props.UCO }</li>
                    <li class="list-group-item">VaVId : { props.VaVId }</li>
                </ul>
            </Card.Body>
        </Card>
    ) 
}

/*
 * @param props.id
 * @param props.name
 * @param props.surname
 * @param props.email
 * @param props.lastchange
 * @param props.externalId
 * @param props.UCO
 * @param props.VaVId
 * @return 
 */
export const UserModelTableRow = (props) =>  {
    return (
        <tr>
            <td><UserModelSmall {...props} /></td>
            <td> <a href={'mailto:' + props.email} >✉</a> { props.email }</td>
            <td>{ props.UCO }</td>
            <td>{ props.VaVId } / { props.externalId }</td>
        </tr>
    ) 
}

/*
 * @return 
 */
export const UserModelTableHeadRow = (props) =>  {
    return (
        <tr>
            <th>Jméno</th>
            <th>email</th>
            <th>UCO</th>
            <th>Odkazy</th>
        </tr>
    ) 
}

/*
 * @param props.data is array of UserModel
 * @return 
 */
export const UserModelTable = (props) =>  {
    const rows = props.data.map(
        (item, index) => <UserModelTableRow key={'k' + index} {...item}/>
        );

    return (
        <Table size="sm">
            <thead>
                <UserModelTableHeadRow />
            </thead>
            <tbody>
                {rows}
            </tbody>
        </Table>
    ) 
}

const UserStudyPlans = (props) => {
    if (props.studyplanitemteachermodels) {
        let items = [];
        for(let item of props.studyplanitemteachermodels){
            let id = item.studyplanitemmodel.studyplanId
            if (!items.includes(id)){
                items.push(id)
            }
        }
        //return (<br/>)
        //return (<>{JSON.stringify(props.studyplanitemteachermodels)}</>)
        return (
            <Row>
            {items.map(id=>(
                <Col xs={6} md={4}>
                    <StudyPlanModelFetching id={id} as={StudyPlanModelMediumForUser}/>
                </Col>
            ))}
            </Row>
        )
    } else {
        return <br/>
    }
}

/*
 * @param props holds all data needed for proper rendering
 * @return 
 */
export const UserModelLarge = (props) =>  {
    const groups = props.usergroupmodels.map((usergroup) => usergroup.groupmodel)

    return (
        <>
        <Row>
            <Col>
                <Card>
                <Card.Header className='bg-light bg-gradient'>
                    <Card.Title>
                        🧍 { props.name } { props.surname } ({ props. UCO }) <a href={'mailto:' + props.email}>✉</a>
                    </Card.Title>
                </Card.Header>
                <Card.Body>
                    <GroupModelTable data={groups}/>
                </Card.Body>
                <Card.Body>
                    <UserStudyPlans {...props} />
                </Card.Body>
                </Card>
            </Col>
        </Row>
        </>
    ) 
}

/*
 * @param props holds all data needed for proper rendering
 * @param props.as defines the Component for proper rendering
 * @return 
 */
export const UserModelFetching = (props) => {
    const [state, error] = useQueryGQL(props.id, QueryUserModelByidLarge, (response) => response.data.usersById, [props.id])
    const Component = props.as
    if (state !== null) {
        return <Component {...props} {...state} />
    } else if (error !== null) {
        return <LoadingError error={error} />
    } else {
        return <Loading>{props.id}</Loading>
    }
}
    
/*
 * @param props holds extra properties
 * @return 
 */
export const UserModelPage = (props) => {
    const { id } = useParams();

    return (
        <UserModelFetching {...props} id={id} as={UserModelLarge}/>
    )    

}  