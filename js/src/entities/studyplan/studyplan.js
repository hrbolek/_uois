import {
    Link,
    useParams
  } from "react-router-dom";
import { useEffect, useState } from "react";
import Row from 'react-bootstrap/Row';
import Col from 'react-bootstrap/Col';
import Card from 'react-bootstrap/Card';
import Table from 'react-bootstrap/Table';

import { useQueryGQL, LoadingError, Loading } from '../index';
import { root, rootGQL } from '../config';
import { StudyPlanItemModelLarge, StudyPlanItemModelTable } from './studyplanitem';
import { GroupModelMedium, GroupModelSmall } from "../group/group";

/*
 * @param id holds value for unique entity identification
 * @return Future with response from gQL server
 */
export const QueryStudyPlanModelByidLarge = (id) => 
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
                studyplansById(id: "${id}") {
                    id
                    externalId
                    name
                    studyplanitemmodels {
                      id
                      priority
                      name
                      studyplanitemteachermodels {
                        usermodel {
                          id
                          name
                          surname
                        }
                      }
                                    }
                    studyplangroupsmodels {
                      id
                      groupmodel {
                        id
                        name
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
export const QueryStudyPlanModelByidMedium = (id) => 
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
                studyplansById(id: ${id}) {
                    id
                    name
                    externalId
                }
            }
            `        
        }) // body data type must match "Content-Type" header
    });    

const entityRoot = root + '/studyplans';

/*
 * @param props.id unique identification
 * @param props.name visual representation of item
 * @param props.label visual representation of item
 * @param props.children embeded items
 * @return 
 */
export const StudyPlanModelSmall = (props) =>  {
    if (props.name) {
        return (
            <Link to={entityRoot + `/${props.id}`}>📜 {props.name}{props.children}</Link>
        )
    } else if (props.label) {
        return (
            <Link to={entityRoot + `/${props.id}`}>📜 {props.label}{props.children}</Link>
        )
    } else {
        return (
            <Link to={entityRoot + `/${props.id}`}>📜 {props.id}{props.children}</Link>
        )
    } 
}



const StudyPlanItems = (props) => {

    if (props.studyplanitemmodels) {
        const items = props.studyplanitemmodels.map((item, index) => item.studyplanitem);
        return (
            <StudyPlanItemModelTable data={props.studyplanitemmodels} />
        )
    } else {
        return null
    }
}

/*
 * @param props holds all data needed for proper rendering
 * @return 
 */
export const StudyPlanModelMediumForGroup = (props) =>  {
    return (
        <Card>
            <Card.Header className='bg-success bg-light bg-gradient text-white'>
                <Card.Title><StudyPlanModelSmall {...props} /> ({ props.externalId })</Card.Title>
            </Card.Header>
            <Card.Body>
                <StudyPlanItems {...props}/>
            </Card.Body>
        </Card>
    ) 
}


const StudyPlanGroups = (props) => {
    if (props.studyplangroupsmodels) {
        return (
            <Row>
                {props.studyplangroupsmodels.map((item, index) => (
                    <Col xs={6} md={4}>
                        <GroupModelSmall {...item.groupmodel}/>
                    </Col>
                ))}
            </Row>
        )
    } else {
        return null
    }
}

/*
 * @param props holds all data needed for proper rendering
 * @return 
 */
export const StudyPlanModelMediumForUser = (props) =>  {
    return (
        <Card>
            <Card.Header className='bg-success bg-light bg-gradient text-white'>
                <Card.Title><StudyPlanModelSmall {...props} /> ({ props.externalId })</Card.Title>
            </Card.Header>
            <Card.Body>
                <StudyPlanGroups {...props}/>
            </Card.Body>
        </Card>
    ) 
}

export const StudyPlanModelMedium = (props) =>  {
    const Component = props.as
    return (
        <Component {...props} />
    ) 
}

/*
 * @param props.id
 * @param props.name
 * @param props.externalId
 * @return 
 */
export const StudyPlanModelTableRow = (props) =>  {
    return (
        <tr>
            <td>{ props.id }</td>
            <td>{ props.name }</td>
            <td>{ props.externalId }</td>
        </tr>
    ) 
}

/*
 * @return 
 */
export const StudyPlanModelTableHeadRow = (props) =>  {
    return (
        <tr>
            <th><StudyPlanModelSmall {...props} /></th>
            <th>name</th>
            <th>externalId</th>
        </tr>
    ) 
}

/*
 * @param props.data is array of StudyPlanModel
 * @return 
 */
export const StudyPlanModelTable = (props) =>  {
    const rows = props.data.map(
        (item, index) => <StudyPlanModelTableRow key={'k' + index} {...item}/>
        );

    return (
        <Table>
            <thead>
                <StudyPlanModelTableHeadRow />
            </thead>
            <tbody>
                {rows}
            </tbody>
        </Table>
    ) 
}

//studyplangroupsmodels

/*
 * @param props holds all data needed for proper rendering
 * @return 
 */
export const StudyPlanModelLarge = (props) =>  {
    let StudyPlanItemModelTableData = []
    if (props.studyplanitemmodels) {
        //StudyPlanItemModelTableData = props.studyplanitemmodels.map(item => )
    }
    return (
        <>
        <Row>
            <Col>
                <Card>
                    <Card.Header className='bg-success bg-gradient text-white'>
                        <Card.Title>📜 { props.name } ({ props. externalId })</Card.Title>
                    </Card.Header>

                    
                    <Card.Body>
                        <StudyPlanGroups {...props}/>
                    </Card.Body>
                    <Card.Body>
                        <StudyPlanItemModelTable data={props.studyplanitemmodels}/>
                    </Card.Body>
                </Card>
            </Col>
        </Row>
        </>
    ) 
}

/*
 * @param props holds all data needed for proper rendering
 * @return 
 */
export const StudyPlanModelFetching = (props) => {
    const [state, error] = useQueryGQL(props.id, QueryStudyPlanModelByidLarge, (response) => response.data.studyplansById, [props.id])
    const Component = props.as;
    if (state !== null) {
        return <Component {...state} />
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
export const StudyPlanModelPage = (props) => {
    const { id } = useParams();

    return (
        <StudyPlanModelFetching {...props} id={id} as={StudyPlanModelLarge}/>
    )    

}  