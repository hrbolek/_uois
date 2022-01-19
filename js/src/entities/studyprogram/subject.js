
import {root} from "../index";

import { Link, useParams } from "react-router-dom";

import { Row, Table, Card, Col} from "react-bootstrap";
import Accordion from "react-bootstrap/Accordion";
import Button from "react-bootstrap/Button";

//import AccordionCollapse from "react-bootstrap/AccordionCollapse";

import React, {Component, useState, useEffect } from "react";

import { PersonSmall } from "../person/person";
import { SubjectSemesterSmall, SubjectSemesterTopicMedium } from "./lesson";
import { useQueryGQL, Loading, LoadingError } from "../index";
import { ProgramSmall } from "./studyprogram";
import { TeacherSmall } from "../person/teacher";

//import { LessonSmall } from "../lesson/lesson";

export const subjectsRoot = root + "/studyprograms/subject"

export const SubjectSmall = (props) => {
    //const ProgID=props.ProgID
    return (
        <Link to={subjectsRoot + `/${props.id}`}>{props.name}{props.children}</Link>
    )   
}

const tableStyle = {
    color: '#333333',
    width: '70%',
    border: '1px solid black',
    'border-collapse': 'collapse',
        
    //'background-color': '#CCCCCC',
    };

export const SubjectLargeAPI = (props) => {
    const { id } = useParams();
    const studyprog=id.split(',')[0]
    const lesson=id.split(',')[1]
    const semestr=id.split(',')[2]
      console.log("id v ClassroomLargeAPI je : ", id)
  
      const [state, setState] = useState(
        {'name': "StudyProgName",
        'subjects' : [{'name':"name", 'id':"id", 'semesters':[{'name':'name','id':'id','topics':[{'name':'name','id':'id'}]}]}]}
      );
      useEffect(() => {
          fetch('/gql', {
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
          <SubjectLarge json={state} ProgID={studyprog} lessonid={lesson} semesterid={semestr}/>
      </div>)
  }
  
export const SubjectMedium = (props) => {
    return (
        <Card>
            <Card.Header>
                { props.name } ({ props.id })
            </Card.Header>
            <Card.Body>
                { props.children }
            </Card.Body>
        </Card>
    )
}

export const SubjectSemesterMedium = (props) => {
    const lessons = props.topics.map((lesson, index) => (
        <Col><SubjectSemesterTopicMedium key={index} {...lesson} /></Col>
    ))
    return (
        <Row xs={12} md={4}>
        {lessons}
        </Row>
    )
}

export const SemesterList = (props) => {
    // see https://codesandbox.io/s/react-bootstrap-multiple-accordion-tabs-oboks
    const semesters = props.semesters.map(semester => (
        <Accordion key={semester.id}>
          <Card>
            <Card.Header>
              <Accordion.Toggle as={Button} variant="link" eventKey={semester.id}>
                {semester.name}
              </Accordion.Toggle>
            </Card.Header>
            <Accordion.Collapse eventKey={semester.id}>
              <Card.Body>
                  <SubjectSemesterMedium {...semester}/>
              </Card.Body>
            </Accordion.Collapse>
          </Card>
        </Accordion>
      ))
    
    return (
        <>
            {semesters}
        </>
    )
}
  
export const SubjectTopicList = (props) => {
    return (
        <Card>
            <Card.Header>
                Seznam témat
            </Card.Header>
            <Card.Body>
                {props.lessons.map((lesson, index) => (
                    <>
                    {lesson.topic}, {lesson.id} <br/>
                    </>
                ))}
            </Card.Body>
        </Card>
    )
}

export const SubjectProgram = (props) => {
    return (
        <Card>
            <Card.Header>
                Program <ProgramSmall {...props.program} />
            </Card.Header>
            <Card.Body>
            {JSON.stringify(props.program)}
            </Card.Body>
        </Card>
    )
}

export const SubjectGrants = (props) => {
    return (
        <Card>
            <Card.Header>
                Garanti
            </Card.Header>
            <Card.Body>
                <TeacherSmall id={1} name={'Alexandr'} surname={'Štefek'}/>
            </Card.Body>
        </Card>
    )
}

export const SubjectLarge = (props) => {
    return (
        <Card>
            <Card.Header>
                Předmět {props.name} ({props.id})
            </Card.Header>
            <Card.Body>
                <Row>
                    <Col md={3}>
                        <SubjectProgram {...props} /> <br/>
                        <SubjectGrants {...props} />
                    </Col>
                    <Col md={6}>
                        <SubjectTopicList {...props} />
                    </Col>
                    <Col md={3}>
                        <SubjectProgram {...props} />
                    </Col>
                </Row>
            </Card.Body>
        </Card>
    )
}

  export const SubjectLarge_ = (props) => {
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
                if(props.semesterid===sgItem2.id){
                    for(var index3 = 0; index3 < json.subjects[index].semesters[index2].topics.length; index3++) {
                        const sgItem3 = json.subjects[index].semesters[index2].topics[index3]
                        topics.push(<i><SubjectSelectedMed name={sgItem3.name} semesterid={sgItem2.id} lessonid={sgItem.id} ProgID={props.ProgID} topicid={sgItem3.id}/></i>);
                    }
                }                
              //topics.push(<b>------------------------------------------------další---semestr---------------------------------------------------</b>)
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
    </Card>
      
      )
  }
  
  export const SubjectSelectedMed = (props) => {
  
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

export const SubjectLargeStoryBook = (props) => {
    const extraProps = {}
    return <SubjectLarge {...extraProps} {...props} />
}

export const SubjectLargeQuery = (id) => 
    fetch('/gql', {
        method: 'POST',
        headers: {
        'Content-Type': 'application/json',
        },
        body: JSON.stringify({
        query: `
        query{
            subject(id: ${id}) {
                id
                name
                lessons {
                  id
                  topic
                }
                program {
                  id
                  name
                }
              }
        }              
            `,
        variables: {
            now: new Date().toISOString(),
        },
        }),
    })
    
export const SubjectPageFetching = (props) => {
    const [state, error] = useQueryGQL(props.id, SubjectLargeQuery, (response) => response.data.subject, [props.id])
    
    if (error != null) {
        return <LoadingError error={error} />
    } else if (state != null) {
        return <SubjectLargeStoryBook {...state} />
    } else {
        return <Loading>Předmět {props.id}</Loading>
    }
}

export const SubjectPage = (props) => {
    const { id } = useParams()

    return <SubjectPageFetching {...props} id={id} />
}