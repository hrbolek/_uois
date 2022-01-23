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

export const progRoot = root + "/studyprograms";


export const ProgramSmall = (props) => {
    return(
        <Link to={progRoot + `/program/${props.id}`}>{props.name}{props.children}</Link>
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
                Garanti
            </Card.Header>
            <Card.Body>
            </Card.Body>
        </Card>
    )
}

export const ProgramStudents = (props) => {
    return (
        <Card>
            <Card.Header>
                Studenti
            </Card.Header>
            <Card.Body>
                {props.students.map((student, index) => <><StudentSmall {...student.person}/><br/></>)}
            </Card.Body>
        </Card>
    )
}

export const ProgramLarge = (props) => {
    return (        
            <Card>
                <Card.Header>
                    Program {props.name} ({props.id})
                </Card.Header>
                <Card.Body>
                    <Row>
                        <Col md={3}>
                            <ProgramGrants {...props} />
                        </Col>
                        <Col md={6}>
                            <ProgramSubjectList {...props} />        
                        </Col>
                        <Col md={3}>
                            <ProgramStudents {...props} />        
                        </Col>          
                    </Row>
                </Card.Body>
                <Card.Body>
                    {JSON.stringify(props)}
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
                Předměty
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

export const ProgramLargeStoryBook = (props) => {
    const extraProps = {
        "id": "1",
        "name": "Kyberneticka bezpecnost",
        "subjects": [
          { "id": "1", "name": "Kyberneticka bezpecnost / Předmět 1" },
          { "id": "2", "name": "Kyberneticka bezpecnost / Předmět 2" },
          { "id": "3", "name": "Kyberneticka bezpecnost / Předmět 3" },
          { "id": "4", "name": "Kyberneticka bezpecnost / Předmět 4" },
          { "id": "5", "name": "Kyberneticka bezpecnost / Předmět 5" },
        ],
        "students": [
          { "person": { "id": "85", "name": "Petr Alena", "surname": "Novotná", "email": "Petr.Alena.Novotná@F1.university.world" }          },
          { "person": { "id": "88", "name": "Jaroslav Miroslav", "surname": "Pospíšilová", "email": "Jaroslav.Miroslav.Pospíšilová@F1.university.world" } },
          { "person": { "id": "108", "name": "Zdeněk Věra", "surname": "Marek", "email": "Zdeněk.Věra.Marek@F1.university.world" }          },
          { "person": { "id": "109", "name": "Eva Jiří", "surname": "Novotná", "email": "Eva.Jiří.Novotná@F1.university.world" }           },
          { "person": { "id": "144", "name": "Lenka Hana", "surname": "Horáková", "email": "Lenka.Hana.Horáková@F1.university.world" }          },
          { "person": { "id": "146", "name": "Lucie Jan", "surname": "Dvořák", "email": "Lucie.Jan.Dvořák@F1.university.world" }          },
          { "person": { "id": "151", "name": "Lenka Jakub", "surname": "Kučera", "email": "Lenka.Jakub.Kučera@F1.university.world" }},
        ]
      }
    return <ProgramLarge {...extraProps} {...props} />
}

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

export const StudyProgramLargeFetching = (props) => {
    const [state, error] = useQueryGQL(props.id, StudyProgramLargeQuery, (response) => response.data.program, [props.id])
    
    if (error != null) {
        return <LoadingError error={error} />
    } else if (state != null) {
        return <ProgramLargeStoryBook {...state} />
    } else {
        return <Loading>program {props.id}</Loading>
    }
 
}

export const StudyProgramPage = (props) => {
    const { id }  = useParams();

    return <StudyProgramLargeFetching {...props} id={id} />
}