import {root} from "../index";

//import {SubjectSmall} from "../subject/subject";
//import {LessonSmall} from "../lesson/lesson";
import { Link } from "react-router-dom";

import Card  from "react-bootstrap/Card";
import Row from "react-bootstrap/Row";
import Col from "react-bootstrap/Col";
import Table from "react-bootstrap/Table";
import Accordion from "react-bootstrap/Accordion";
import Button from "react-bootstrap/Button";

import {useParams } from "react-router-dom";

import React, { useState, useEffect } from "react";
//import {LessonSmall} from "../lesson/lesson";

import { TeacherSmall } from "../person/teacher";
import { DepartmentSmall } from "../group/department";
import { FacultySmall } from "../group/faculty";

import { SubjectMedium, SubjectLarge } from "./subject";
import { useQueryGQL, Loading, LoadingError } from "../index";
import { SubjectSmall } from "./subject";
import { StudentSmall } from "../person/student";
import { GroupSmall } from "../group/group";


/** @module StudyProgram */


export const progRoot = root + "/studyprograms";


export const ProgramSmall = (props) => {
    return(
        <Link to={progRoot + `/program/${props.id}`}>{props.children} {props.name}</Link>
    )
}

// export const ProgLargeAPI = (props) => {
//     const [state, setState] = useState(
//         {
//             'programy':[{'id':'id',
//             'name':'name',
//             'subjects':[{'id':'id','name':'name','semesters':[{'id':'id','name':'name'}]}]
//         }]}
//     );
//     useEffect(() => {
//         fetch('http://localhost:50001/gql', {
//             method: 'POST',
//             headers: {
//               'Content-Type': 'application/json',
//             },
//             body: JSON.stringify({
//               query: `
//               # Write your query or mutation here
//               query{
//                 program(id:1){
//                   id
//                   name
//                   subjects{
//                     id
//                     name
//                     semesters{
//                       name
//                       id
//                     }
//                   }
//                 }
//               }       
//                 `,
//               variables: {
//                 now: new Date().toISOString(),
//               },
//             }),
//           })
//             .then((res) => res.json())
//             .then((result) => setState(result.data));
            
//     }, [] )
    
//     //POTOM BUDE: [props.id] - závislost kdy se udělá fetch (vždy když změníme id)!
//     //console.log("po fetchi:", state)
//     return(
//         <div>
//             <ProgLarge json={state}/>
//         </div>
//     )
// }



export const ProgramGrants = (props) => {
    return (
        <Card>
            <Card.Header>
                <Card.Title> Garanti </Card.Title>
                
            </Card.Header>
            <Card.Body>
                <TeacherSmall id={1} name={'Josef Marie'} surname={'Krejčí'} />
            </Card.Body>
        </Card>
    )
}

export const ProgramGroups = (props) => {
    return (
        <Card>
            <Card.Header>
                <Card.Title> Skupiny </Card.Title>
            </Card.Header>
            <Card.Body>
                {props.groups.map((group, index) => <><GroupSmall {...group}/><br/></>)}
            </Card.Body>
        </Card>
    )
}

export const ProgramAppLink = (props) => {
    return (
        <Card>
            <Card.Header>
                <Card.Title> Link na akreditace </Card.Title>
            </Card.Header>
            <Card.Body>
                <a href={'https://apl.unob.cz/Akreditace2017/StudijniProgram/9'} >aplikace akreditace </a>
            </Card.Body>
        </Card>
    )
}

export const ProgramLarge = (props) => {
    return (        
            <Card>
                <Card.Header>
                    <Card.Title>
                    Program {props.name} ({props.id})
                    </Card.Title>
                </Card.Header>
                <Card.Body>
                    <Row>
                        <Col md={3}>
                            <ProgramGrants {...props} /> <br/>
                            <ProgramAppLink {...props} />   
                        </Col>
                        <Col md={6}>
                            <ProgramSubjectList {...props} />        
                        </Col>
                        <Col md={3}>
                            <ProgramGroups {...props} />   <br/>
                        </Col>          
                    </Row>
                </Card.Body>
                <Card.Body>
                    
                </Card.Body>

            </Card>
            
    )
}

export const ProgramLarge_ = (props) => {
    const json=props.json


    //setState(props)
    console.log("----obsah props:--- ", json)

    /*
    const programy = []
    for(var index = 0; index < json.program.length; index++) {
        const sgItem = json.program[index]
        programy.push(<ProgMedium name={sgItem.name} id={sgItem.id}/>);
    }
*/
try{ 
    if(json.program.length>1){
        const programy = []
        for(var index = 0; index < json.program.length; index++) {
            const sgItem = json.program[index]
            programy.push(<ProgramMedium name={sgItem.name} id={sgItem.id}/>);
        }
        return (<div>
            <Table striped bordered hover>
                <thead>
                    <h3>Seznam studijních programů:</h3>
                </thead>
              {programy}                  
            </Table>
            
            {/*<p><b>fetchnuty JSON soubor z GraphQL:</b> {JSON.stringify(json)}</p>*/}

        </div>)
    
        }
        else{
            return(<div>
                <Table striped bordered hover>
                    <thead>
                        <h3>Studijní program:</h3>
                    </thead>
                        
                  <Card><ProgramMedium name={json.program.name} id={json.program.id}/></Card>             
                </Table>
                
                {/*<p><b>fetchnuty JSON soubor z GraphQL:</b> {JSON.stringify(json)}</p>*/}

            </div>)
        }

} catch(e) { 
    console.error(e); 
    return(<div>
        <Table striped bordered hover>
            <thead>
                <h3>Studijní program:</h3>
            </thead>
              
          <Card><ProgramMedium name={json.programy.name} id={json.programy.id}/></Card>             
        </Table>
        
        {/*<p><b>fetchnuty JSON soubor z GraphQL:</b> {JSON.stringify(json)}</p>*/}

    </div>)
    
}


//console.log("obsah program: ",programy)
    
}

const tdStyle = {
    'colspan': "2",
    'align': "right",
    
    
    //'background-color': '#CCCCCC',
    };

const tableStyle = {
    color: '#333333',
    width: '110%',
    border: '1px solid black',
    'border-collapse': 'collapse',
        
    //'background-color': '#CCCCCC',
    };

export const ProgramSubjectList_ = (props) => {
    return (
        <Table >
            <thead>
                <tr><td>Předměty</td></tr>
            </thead>
            <tbody>
                <tr><td>{JSON.stringify(props)}</td></tr>
            </tbody>
        </Table>
    )
}

export const ProgramSubjectList = (props) => {
    // see https://codesandbox.io/s/react-bootstrap-multiple-accordion-tabs-oboks
    // see https://react-bootstrap.github.io/components/accordion/
    if (!props.subjects) {
        return (
            <>
            NO subjects
            </>
        )
    }

    // const subjects = props.subjects.map((subject, index) => (      
    //     <Accordion.Item eventKey={index + ""}>
    //         <Accordion.Header>{subject.name}</Accordion.Header>
    //         <Accordion.Body>
    //             <SubjectMedium {...subject}/>
    //         </Accordion.Body>
    //     </Accordion.Item>
    //   ));
    // const subjects = props.subjects.map((subject, index) => (
    //     <Accordion key={subject.id} >
    //     <Card>
    //         <Card.Header>
    //             <Accordion.Toggle as={Button} variant="link" eventKey={subject.id}>
    //                 {subject.name} ({subject.id})
    //             </Accordion.Toggle>
    //         </Card.Header>
            
    //         <Accordion.Collapse eventKey={subject.id}>
    //             <Card.Body>
    //                 <SubjectLarge {...subject}/>
    //             </Card.Body>
    //         </Accordion.Collapse>
            
    //     </Card>
    //     </Accordion>
    // ))


    return (
        <Card>
            <Card.Header>
                <Card.Title> Předměty </Card.Title>
                
            </Card.Header>
            <Card.Body>
                {props.subjects.map((subject, index) => (
                    <>
                        <SubjectSmall {...subject} />
                        <br/>
                    </>
                )
                )}
            </Card.Body>
        </Card>
    )
}
  


export const ProgramMedium = (props) => {
    return (
        <Card>
            <Card.Header>
                Program {props.name}, typ {'P'} / {'Prezenční'}
            </Card.Header>
            <Card.Body>
                <Row>
                    <Col>
                        Fakulta:
                        <br />
                        <FacultySmall id={13} name={'FVT'} />
                    </Col>
                    <Col>
                        Garant:
                        <br />
                        <TeacherSmall id={15} name={'Petr'} surname={'Novak'} />
                    </Col>
                </Row>
                <Row>
                    <Col>
                        {props.children}
                    </Col>
                </Row>
            </Card.Body>
        </Card>
    )
}
export const ProgramMedium_ = (props) => {

    //VYŘEŠENO zmizení [0]teho prvku ----> ale je to správně ? ---> NENÍ TO NEJLEPŠÍ, NĚKDE SE OBJEVÍ CHYBA !!!
    // const state ={
    //     'name': props.name,
    //     'id': props.id
    // };
    //console.log("ProgMedium state: ", state)
    //useEffect(()=>{})
    return (
            <Table striped bordered hover style={tableStyle}>
            <tbody>
                    <tr>
                        <td>Název: </td>
                        <td><b>{props.name}</b></td>
                        <td>Typ programu: <b>P</b></td>
                        <td>Forma studia: <b>prenzenční</b></td>
                    </tr>
                    <tr>
                        <td>Fakulta: </td>
                        <td><b><DepartmentSmall id={props.id} name={"*FAKULTA*"}/></b></td>
                        <td colSpan="2" align="left">Garant: <b><TeacherSmall id={props.id} name={"ppl. Ing. Luděk Jedlička, Ph.D"}/></b></td>
                    </tr>
                    <tr>
                        <td>id: </td>
                        <td><b>{props.id}</b></td>
                        <td colSpan="2" align="left"> <b><ProgramSmall name="předměty" id={props.id}/></b></td>
                    </tr>
            </tbody>
            </Table>
    )
}

/**
 * Renders a page with data representing a study program, contains predefined data which can are overrided by props
 * @param {*} props 
 * @param {*} props.id - identification
 * @param {string} props.name - name
 * @function
 */
export const ProgramLargeStoryBook = (props) => {
    const extraProps = {
        "id": "1",
        "name": "Kybernetická bezpečnost",
        "subjects": [
          { "id": "1", "name": "Programování" },
          { "id": "2", "name": "Datová analýza" },
          { "id": "3", "name": "Informační bezpečnost" },
          { "id": "4", "name": "Distribované technologie" },
          { "id": "5", "name": "Právní rámec" },
        ],
        "groups": [
          { "id": "7", "name": "23-5KB" },
          { "id": "8", "name": "24-5KB" },
          { "id": "9", "name": "25-5KB" }
        ]
      }
    return <ProgramLarge {...extraProps} {...props} />
}

/**
 * Retrieves the data from GraphQL API endpoint
 * @param {*} id - identificator
 * @function
 */
export const StudyProgramLargeQuery = (id) =>
    fetch('/gql', {
        method: 'POST',
        headers: {
        'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            query: `
            # Write your query or mutation here
            query {
                program(id: ${id}) {
                  id
                  name
                    subjects {
                    id
                    name
                    
                  }
                  
                  students {
                    person {
                      id
                      name
                      surname
                      email
                    }
                  }
                }
              }
            `}),
    })

/**
 * Fetch the data from API endpoint and renders a page representing a study program
 * @param {*} props - extra props for encapsulated components / visualisers
 * @param {*} [props.as = ProgramLargeStoryBook] - ReactJS component (function) which is responsible for rendering
 * @param {*} [props.with = StudyProgramLargeQuery] - function fetching the data and returning promise with the data from API endpoint
 * @function
 */
export const StudyProgramLargeFetching = (props) => {
   
    const Visualizer = props.as || ProgramLargeStoryBook;
    const queryFunc = props.with || StudyProgramLargeQuery;

    const [state, error] = useQueryGQL(props.id, queryFunc, (response) => response.data.program, [props.id])
    
    if (error != null) {
        return <LoadingError error={error} />
    } else if (state != null) {
        return <Visualizer {...props} {...state} />
    } else {
        return <Loading>program {props.id}</Loading>
    }
 
}

/**
 * Renders a page representing a study program, designed as a component for a ReactJS router
 * @param {*} props - extra props for encapsulated components / visualisers
 * @function
 */
export const StudyProgramPage = (props) => {
    const { id }  = useParams();

    return <StudyProgramLargeFetching {...props} id={id} />
}