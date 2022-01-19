
import {root} from "../index";

import { Link, useParams } from "react-router-dom";

import  Card  from "react-bootstrap/Card";
import { Row, Table} from "react-bootstrap";
import React, {Component, useState, useEffect } from "react";

import {SubjectSmall} from "./subject";
import {PersonSmall} from "../person/person";

import { useQueryGQL, Loading, LoadingError } from "../index";
export const lessonRoot = root + "/studyprograms/lesson"

export const SubjectSemesterSmall = (props) => {
    //const ProgID=props.ProgID
    return (
        <Link to={lessonRoot + `/${props.id}`}>{props.name}{props.children}</Link>
    )   
}

const tableStyle = {
    color: '#333333',
    width: '70%',
    border: '1px solid black',
    'border-collapse': 'collapse',
        
    //'background-color': '#CCCCCC',
    };

export const LessonMed = (props) => {

    return(
        <Card.Body>
                <Table striped bordered hover style={tableStyle}>
                    <thead>
                    <tr>                                    
                        <td align="left">Název předmětu: </td>
                        <td colSpan="3" align="center"><SubjectSemesterSmall name={props.name} lessonid={props.lessonid} ProgID={props.ProgID}/></td>
                        <td colSpan="2" align="right">id (id): <b>{props.lessonid}</b> </td>                        
                    </tr>
                    </thead>
                    <tbody>
                    <tr>
                        <td>Semestry: </td>
                        <td colSpan="5"> {props.semesters} </td>
                    </tr>
                    </tbody>
                </Table>
  
        </Card.Body>

    )
}

export const LessonsListLargeAPI = (props) => {
    const { id } = useParams();
    console.log("id v ClassroomTest je : ", id)

    const [state, setState] = useState(
        {'name': "StudyProgName",
        'subjects' : [{'name':"name", 'id':"id", 'semesters':[{'name':'name','id':'id'}]}]}
    );
    useEffect(() => {
        fetch('http://localhost:50001/gql', {
            method: 'POST',
            headers: {
              'Content-Type': 'application/json',
            },
            body: JSON.stringify({
              query: `
              query{
                program(id:`+id+`){
                  name
                  subjects{
                    id
                    name
                    semesters{
                      name
                      id
                    }
                  }
                }
              }             
                `,
              variables: {
                now: new Date().toISOString(),
              },
            }),
          })
            .then((res) => res.json())
            .then((result) => setState(result.data.program));
    }, [id] )
    
    //console.log("State je : ", state)
    console.log("STATE je : ", state)
    return(                                                        //předání testing-->vrácení se zpět na seznam arealů
    <div>   
        <LessonsListLarge json={state} ProgID={id}/>
    </div>)
}


export const LessonsListLarge = (props) => {
    console.log("PROPS:  ", props)
    const json=props.json
    const arealName=props.json.name
    const ProgID=props.ProgID
    
    /*
    const [state, setState] = useState(
        {
            'arealname' : 'props.json.name',
            'countries' : [{'name':'budova', 'code': 'id'}]
        });
    */
    
    const subjects = []
    for(var index = 0; index < json.subjects.length; index++) {
      const semesters = []
      const sgItem = json.subjects[index]
            for(var index2 = 0; index2 < json.subjects[index].semesters.length; index2++) {
                const sgItem2 = json.subjects[index].semesters[index2]
                semesters.push(<i><SubjectSmall name={sgItem2.name} semesterid={sgItem2.id} lessonid={sgItem.id} ProgID={ProgID}/> -||- </i>);
            }
        subjects.push(<LessonMed name={sgItem.name} lessonid={sgItem.id} semesters={semesters} ProgID={ProgID}/>);
    }
    //console.log("buldings = ", state)
    return(                                                        //předání testing-->vrácení se zpět na seznam arealů
    <div>   
      <Card>
      <Card.Header><h1>Seznam předmětů ve studijním programu <i>{arealName}</i>: </h1></Card.Header>
            {subjects}
      </Card>   
            {/*<p><b>fetchnuty JSON soubor z GraphQL:</b> {JSON.stringify(json)}</p>*/}
    </div>)
}


///************---------------------------------------------------------------------------------------******************/


export const LessonLargeAPI = (props) => {
  const { id } = useParams();
  const studyprog=id.split(',')[0]
  const lesson=id.split(',')[1]
    console.log("id v ClassroomLargeAPI je : ", id)

    const [state, setState] = useState(
      {'name': "StudyProgName",
      'subjects' : [{'name':"name", 'id':"id", 'semesters':[{'name':'name','id':'id','topics':[{'name':'name','id':'id'}]}]}]}
    );
    useEffect(() => {
        fetch('http://localhost:50001/gql', {
            method: 'POST',
            headers: {
              'Content-Type': 'application/json',
            },
            body: JSON.stringify({
              query: `
              query{
                program(id:`+studyprog+`){
                  name
                  subjects{
                    id
                    name
                    semesters{
                      name
                      id
                      topics{
                        name
                        id
                      }
                    }
                  }
                }
              }              
                `,
              variables: {
                now: new Date().toISOString(),
              },
            }),
          })
            .then((res) => res.json())
            .then((result) => setState(result.data.program));
    }, [id] )
    
    //console.log("State je : ", state)
    console.log("STATE je : ", state)
    return(                                                        //předání testing-->vrácení se zpět na seznam arealů
    <div>   
        <LessonLarge json={state} ProgID={studyprog} lessonid={lesson}/>
    </div>)
}


export const LessonLarge = (props) => {
    //console.log("id v ClassroomTest je : ", id)
    console.log("PROPS:  ", props)
    const json=props.json
    const programName=props.json.name
    var temaname="empty"
    
    /*
    const [state, setState] = useState(
        {
            'arealname' : 'props.json.name',
            'countries' : [{'name':'budova', 'code': 'id'}]
        });
    */
    
        const subjects = []
        const semesters = []
        for(var index = 0; index < json.subjects.length; index++) {
          const topics = []
          const sgItem = json.subjects[index]
          if(props.lessonid===sgItem.id){
            for(var index2 = 0; index2 < json.subjects[index].semesters.length; index2++) {
              const sgItem2 = json.subjects[index].semesters[index2]
              for(var index3 = 0; index3 < json.subjects[index].semesters[index2].topics.length; index3++) {
                const sgItem3 = json.subjects[index].semesters[index2].topics[index3]
                topics.push(<i><LessonSelectedMed name={sgItem3.name} semesterid={sgItem2.id} lessonid={sgItem.id} ProgID={props.ProgID} topicid={sgItem3.id}/></i>);
            }
            topics.push(<div><h3><b> ♣ další semestr:</b></h3></div>)
              semesters.push(<i><SubjectSmall name={sgItem2.name} semesterid={sgItem2.id} lessonid={sgItem.id} ProgID={props.ProgID}/> -||- </i>);
          }
          subjects.push(topics);
          temaname=sgItem.name
          }
                
        }
        
    return(                                                       
    <Card>   
      <Card.Header><h1>Informace o předmětu <i><SubjectSemesterSmall name={temaname} ProgID={props.ProgID} lessonid={props.lessonid}/></i>: </h1></Card.Header>
      <Card>
            <Table>
            <Card.Body>
                
                    <td>Garant pro studijní program "{programName}" : </td>
                    <td><h3>*<PersonSmall id={props.id} name={"*garant*"}/>*</h3></td>
                
            </Card.Body>
            <Card.Body>
                
                    <td>Semestry: </td>
                    <td><b>{semesters}  (filtr podle semestru)</b></td>
                    
                
                <br/>
          </Card.Body>    
            </Table>
      </Card>
      <Card>
      <Card.Header><h3>Seznam lekcí(témat):</h3></Card.Header>
            <Card>{subjects}</Card>
      </Card>
            {/*<p><b>fetchnuty JSON soubor z GraphQL:</b> {JSON.stringify(json)}</p>*/}
    </Card>)
}

export const LessonSelectedMed = (props) => {

    return(
        <Card>
          
                <Table striped bordered hover style={tableStyle}>
                    <thead>
                    <tr>                                    
                        <td align="left">Název tématu: </td>
                        <td colSpan="3" align="left"> {props.name} </td>
                        <td colSpan="2" align="right">id (id): <b>{props.topicid}</b> </td>                        
                    </tr>
                    </thead>
                    <tbody>
                    <tr>                                    
                        <td align="left">Vyučující: </td>
                        <td colSpan="5" align="left"> {/*props.name*/}  -  
                        <PersonSmall id={props.topicid+"/1"} name={"vyučující1 "}/> -||-
                        <PersonSmall id={props.topicid+"/2"} name={"vyučující2 "}/> -||-
                        <PersonSmall id={props.topicid+"/3"} name={"vyučující3 "}/> </td>                      
                    </tr>
                    </tbody>
                </Table>
  
        </Card>

    )
}

export const SubjectSemesterTopicMedium = (props) => {
    return (
        <Card>
            <Card.Header>
                SubjectSemesterTopicMedium
            </Card.Header>
            <Card.Body>
                {JSON.stringify(props)}
            </Card.Body>
        </Card>
    )
}

export const SubjectSemesterTopicLarge = (props) => {
    return (
        <SubjectSemesterTopicMedium {...props} />
    )
}

export const SubjectSemesterTopicLargeStoryBook = (props) => {
    const extraProps = {}
    return (
        <SubjectSemesterTopicLarge {...extraProps} {...props}/>
    )
}

export const SubjectSemesterTopicLargeQuery = (id) => 
    fetch('/gql', {
                method: 'POST',
                headers: {
                'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                query: `
                query {
                    subjectSemesterTopic(id:${id}) {
                        id
                        name
                        subjectsemester {
                          id
                          name
                          subject {
                            id
                            name
                          }
                        }
                      }     
                    }               
                    `,
                variables: {
                    now: new Date().toISOString(),
                },
                }),
            })

export const SubjectSemesterTopicLargeFetching = (props) => {
    const [state, error] = useQueryGQL(props.id, SubjectSemesterTopicLargeQuery, (response) => response.data.subject, [props.id])
    
    if (state != null) {
        return <SubjectSemesterTopicLargeStoryBook {...state} />
    } else if (error != null) {
        return <LoadingError error={error} />
    } else {
        return <Loading>Předmět {props.id}</Loading>
    }
}

export const SubjectSemesterTopicPage = (props) => {
    const { id } = useParams()
    return (
        <SubjectSemesterTopicLargeFetching {...props} id={id} />
    )
}
