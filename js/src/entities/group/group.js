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
import { UserModelSmall, UserModelTable } from '../user/user';
import { StudyPlanModelFetching, StudyPlanModelMediumForGroup } from '../studyplan/studyplan';

/*
 * @param id holds value for unique entity identification
 * @return Future with response from gQL server
 */
export const QueryGroupModelByidLarge = (id) => 
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
                groupsById(id: "${id}") {

                    id
                    name
                    abbreviation
                    lastchange
                    entryYearId
                    externalId
                    UIC
                    grouptypeId

                    grouptypemodel {
                        id
                        name
                    }

    								groupconnectionmodels {
                        id
                        childId
                        parentId
                        groupmodel {
                          id
                          name
                        }
                    }

    								usergroupmodels {
                        id
                        userId
                        usermodel {
                          id
                          name
                          surname
                          email
                        }
                    }
    
                    rolemodels {
    
                        id
                        name
                        lastchange
                        roletypeId
                        userId
                        usermodel {
                          id
                          name
                          surname
                          email
                        }
                        
                    }
                    eventgroupmodels {
                        eventId
                      	eventmodel {
                          	id
                          	label
                          	start
                          	end
                        }
                    }
                    studyplangroupsmodels {
                        studyplanmodel {
                          id
                          name
                        }
                    }
                    studyplanitemgroupmodels {
                        id
                        studyplanitemId
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
export const QueryGroupModelByidMedium = (id) => 
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
                groupById(id: ${id}) {
                    id
                    name
                    abbreviation
                    lastchange
                    entryYearId
                    externalId
                    UIC
                    grouptype_id
                }
            }
            `        
        }) // body data type must match "Content-Type" header
    });    

const entityRoot = root + '/groups';

/*
 * @param props.id unique identification
 * @param props.name visual representation of item
 * @param props.label visual representation of item
 * @param props.children embeded items
 * @return 
 */
export const GroupModelSmall = (props) =>  {
    if (props.name) {
        return (
            <Link to={entityRoot + `/${props.id}`}>👥 {props.name}{props.children}</Link>
        )
    } else if (props.label) {
        return (
            <Link to={entityRoot + `/${props.id}`}>👥 {props.label}{props.children}</Link>
        )
    } else {
        return (
            <Link to={entityRoot + `/${props.id}`}>👥 {props.id}{props.children}</Link>
        )
    } 
}

/*
 * @param props holds all data needed for proper rendering
 * @return 
 */


/*
                    <li class="list-group-item">id : { props.id }</li>
                    <li class="list-group-item">name : { props.name }</li>
                    <li class="list-group-item">abbreviation : { props.abbreviation }</li>
                    <li class="list-group-item">lastchange : { props.lastchange }</li>
                    <li class="list-group-item">entryYearId : { props.entryYearId }</li>
                    <li class="list-group-item">externalId : { props.externalId }</li>
                    <li class="list-group-item">UIC : { props.UIC }</li>
                    <li class="list-group-item">grouptype_id : { props.grouptype_id }</li>
*/
export const GroupModelMedium = (props) =>  {
    return (
        <Card>
            <Card.Header className='bg-light bg-gradient text-white'>
                <Card.Title><GroupModelSmall {...props} /> </Card.Title>
            </Card.Header>
            <Card.Body>
                <ul class="list-group">
                </ul>
            </Card.Body>
        </Card>
    ) 
}

/*
 * @param props.id
 * @param props.name
 * @param props.abbreviation
 * @param props.lastchange
 * @param props.entryYearId
 * @param props.externalId
 * @param props.UIC
 * @param props.grouptype_id
 * @return 
 */
export const GroupModelTableRow = (props) =>  {
    return (
        <tr>
            <td>{ props.id }</td>
            <td><GroupModelSmall {...props} /></td>
            <td>{ props.abbreviation }</td>
            <td>{ props.lastchange }</td>
            <td>{ props.entryYearId }</td>
            <td>{ props.externalId }</td>
            <td>{ props.UIC }</td>
            <td>{ props.grouptype_id }</td>
        </tr>
    ) 
}

/*
 * @return 
 */
export const GroupModelTableHeadRow = (props) =>  {
    return (
        <tr>
            <th>id</th>
            <th>name</th>
            <th>abbreviation</th>
            <th>lastchange</th>
            <th>entryYearId</th>
            <th>externalId</th>
            <th>UIC</th>
            <th>grouptype_id</th>
        </tr>
    ) 
}

/*
 * @param props.data is array of GroupModel
 * @return 
 */
export const GroupModelTable = (props) =>  {
    const rows = props.data.map(
        (item, index) => <GroupModelTableRow key={'k' + index} {...item}/>
        );

    return (
        <Table>
            <thead>
                <GroupModelTableHeadRow />
            </thead>
            <tbody>
                {rows}
            </tbody>
        </Table>
    ) 
}

const GroupStudyPlans = (props) => {
    if (props.studyplangroupsmodels) {
        let items = [];
        for(let item of props.studyplangroupsmodels){
            let id = item.studyplanmodel.id
            if (!items.includes(id)){
                items.push(id)
            }
        }
        //return (<br/>)
        //return (<>{JSON.stringify(props.studyplanitemteachermodels)}</>)
        return (
            <Row className="g-4">
                
                {items.map(id=>(
                    <Col xs={12} md={12} >
                        <StudyPlanModelFetching id={id} as={StudyPlanModelMediumForGroup}/>
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
//

export const GroupModelLarge = (props) =>  {
    const users = props.usergroupmodels.map(usergroup => usergroup.usermodel);
    return (
        <>
                <Row>
                    <Col xs={4} md={4}>
                <Card>
                    <Card.Header className='bg-success bg-gradient text-white'>
                        <Card.Title>👥 {props.abbreviation} - {props.name} ({props.UIC}))</Card.Title>
                    </Card.Header>
                    <Card.Body>
                    <UserModelTable data={users}/>
                                        </Card.Body>
                </Card>
            </Col>
            <Col xs={8} md={8}>
                <Card>
                    <Card.Header className='bg-success bg-gradient text-white'>
                        <Card.Title>Předměty skupiny</Card.Title>
                    </Card.Header>
                    <Card.Body>
                        <GroupStudyPlans {...props}/>
                    </Card.Body>                    
                </Card>
            </Col>
        </Row>
        </>
    ) 
}

/*
 * @param props.with function querying API
 * @param props.as Component used for rendering
 * @return 
 */
export const GroupModelFetching = (props) => {
    let queryFunc = QueryGroupModelByidLarge;
    if (props.with) {
        queryFunc = props.with
    }
    const [state, error] = useQueryGQL(props.id, queryFunc, (response) => response.data.groupsById, [props.id])
    let Component = GroupModelLarge;
    if (props.as) {
        Component = props.as
    }
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
export const GroupModelPage = (props) => {
    const { id } = useParams();

    return (
        <GroupModelFetching {...props} id={id} />
    )    

}  