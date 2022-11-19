import { Link, useParams } from "react-router-dom";
import Card from "react-bootstrap/Card";

import Row from "react-bootstrap/Row";
import Col from "react-bootstrap/Col";

import { root } from '../../helpers/index';
import { useQueryGQL, Loading, LoadingError } from '../../helpers/index';

export const TeacherSmall = (props) => {
    return (
        <>
        <Link to={root + "/users/teacher/" + (props.id)}>{props.name} {props.surname} </Link>
        <a href={"mailto:" + props.email}><i className="bi bi-envelope"></i></a>
        </>
    )
}

export const GroupSmall = (props) => {
    return (
        <>
        <Link to={root + "/groups/department/" + (props.id)}>{props.name} </Link>
        </>
    )
}

export const TeacherMembership = (props) => {
    const { membership } = props
    return (
            <>
            {membership.map(item => (
                <Row>
                    <Col><b>{item.group.grouptype.name}</b></Col>
                    <Col><GroupSmall {...item.group}/></Col>
                </Row>
            ))}
            </>
    )
}

export function TeacherMedium(props) {
    return (
        <Card>
            <Card.Header>
                <Card.Title>
                    <TeacherSmall {...props}/>
                </Card.Title>

            </Card.Header>
            <Card.Body>
                <TeacherMembership {...props}/>
            </Card.Body>
            <Card.Footer>
                {JSON.stringify(props)}
            </Card.Footer>
        </Card>
    )
}

export const SmallHeader = (props) => {
    return (
        <Row>
            <Col md={6} xs={12}>
                {props.label}
            </Col>
            <Col md={6} xs={12}>
                <div className="float-end">{props.children}</div>
            </Col>
        </Row>
    )
}

export const TeacherSmallTimeTable = (props) => {
    return (
        <Card>
            <Card.Header>
                <Card.Title>
                    <SmallHeader label="Malý rozvrh" {...props}>
                        <span className="btn btn-sm btn-outline-info"><Link to={root + "/users/teacher/timetable/" + (props.id)}><i className="bi bi-calendar-week"></i> Rozvrh</Link></span> 
                    </SmallHeader>
                </Card.Title>
            </Card.Header>
            <Card.Body>
                
                <svg style={{"display": "inline-block",	"width": "100%"}} viewBox="0 0 1280 720" preserveAspectRatio="xMinYMid" width="1280" height="720" xmlns="http://www.w3.org/2000/svg" overflow="hidden">
                    <rect x="1" y="1" width="1280" height="720" style={{"fill":"rgb(127,127,127)", "strokeWidth":"3", "stroke": "rgb(0,0,0)"}} />
                    <rect x="50" y="20" width="300" height="100" style={{"fill":"rgb(127,127,255)", "strokeWidth":"3", "stroke": "rgb(0,0,0)"}} />
                </svg>
                
            </Card.Body>
        </Card>
    )
}

export const TeacherSmallPrograms = (props) => {
    return (
        <Card>
            <Card.Header>
                <Card.Title>
                    <SmallHeader label="Garant programu" {...props}>
                        <span className="btn btn-sm btn-outline-info"><Link to={root + "/users/teacher/grant/" + (props.id)}><i className="bi bi-collection"></i> Garance</Link></span> 
                    </SmallHeader>
                </Card.Title>
            </Card.Header>
            <Card.Body>

            </Card.Body>
        </Card>
    )
}

export const TeacherSmallSubjects = (props) => {
    return (
        <Card>
            <Card.Header>
                <Card.Title>
                    <SmallHeader label="Garant předmětů" {...props}>
                        <span className="btn btn-sm btn-outline-info"><Link to={root + "/users/teacher/grant/" + (props.id)}><i className="bi bi-collection"></i> Garance</Link></span> 
                    </SmallHeader>
                </Card.Title>

            </Card.Header>
            <Card.Body>

            </Card.Body>
        </Card>
    )
}

export const TeacherSmallTeachingSubjects = (props) => {
    return (
        <Card>
            <Card.Header>
                <Card.Title>
                    <SmallHeader label="Výuka předmětů" {...props}>
                        <span className="btn btn-sm btn-outline-info"><Link to={root + "/users/teacher/timetable/" + (props.id)}><i className="bi bi-book"></i> Výuka</Link></span> 
                    </SmallHeader>

    
                </Card.Title>
            </Card.Header>
            <Card.Body>

            </Card.Body>
        </Card>
    )
}

export const TeacherSmallPhDs = (props) => {
    return (
        <Card>
            <Card.Header>
                <Card.Title>
                    <SmallHeader label="Školitel" {...props}>
                        <span className="btn btn-sm btn-outline-info"><Link to={root + "/users/teacher/supervisor/" + (props.id)}><i className="bi bi-people"></i> Školitel</Link></span> 
                    </SmallHeader>
                </Card.Title>
            </Card.Header>
            <Card.Body>

            </Card.Body>
        </Card>
    )
}

export const TeacherSmallThesis = (props) => {
    return (
        <Card>
            <Card.Header>
                <Card.Title>
                    <SmallHeader label="Vedoucí prací" {...props}>
                        <span className="btn btn-sm btn-outline-info"><Link to={root + "/users/teacher/supervisor/" + (props.id)}><i className="bi bi-people"></i> Školitel</Link></span> 
                    </SmallHeader>

    
                </Card.Title>

            </Card.Header>
            <Card.Body>

            </Card.Body>
        </Card>
    )
}

export const TeacherLarge = (props) => {
    return (
        <Card>
            <Card.Header>
                <Card.Title>
                    <TeacherHeader label="" {...props} />
                </Card.Title>
            </Card.Header>
            <Card.Body>
                <Row>
                    <Col md={3}>
                        <TeacherMedium {...props} />
                    </Col>
                    <Col md={6}>
                        <TeacherSmallTimeTable {...props} />
                    </Col>
                    <Col md={3}>
                        <TeacherSmallPrograms {...props} />
                        <TeacherSmallSubjects {...props} />
                        <TeacherSmallTeachingSubjects {...props} />
                        <TeacherSmallPhDs {...props} />
                        <TeacherSmallThesis {...props} />
                    </Col>
                </Row>
            </Card.Body>
            <Card.Footer>
                {JSON.stringify(props)}
            </Card.Footer>
        </Card>
    )
}

export const TeacherLargeStoryBook = (props) => {
    return (
        <TeacherLarge {...props} />
    )
}

export const TeacherPageLinks = (props) => {
    return (
        <>
            <span className="btn btn-sm btn-outline-info"><Link to={root + "/users/teacher/timetable/" + (props.id)}><i className="bi bi-calendar-week"></i> Rozvrh</Link></span> 
            <span className="btn btn-sm btn-outline-info"><Link to={root + "/users/teacher/tasks/" + (props.id)}><i className="bi bi-card-checklist"></i> Úkoly</Link></span> 
            <span className="btn btn-sm btn-outline-info"><Link to={root + "/users/teacher/requests/" + (props.id)}><i className="bi bi-envelope"></i> Zprávy</Link></span> 
            <span className="btn btn-sm btn-outline-info"><Link to={root + "/users/teacher/groups/" + (props.id)}><i className="bi bi-book"></i> Výuka</Link></span> 
            <span className="btn btn-sm btn-outline-info"><Link to={root + "/users/teacher/supervisor/" + (props.id)}><i className="bi bi-people"></i> Školitel</Link></span> 
            <span className="btn btn-sm btn-outline-info"><Link to={root + "/users/teacher/grant/" + (props.id)}><i className="bi bi-collection"></i> Garance</Link></span> 
            <span className="btn btn-sm btn-outline-info"><Link to={root + "/users/teacher/timetable/" + (props.id)}><i className="bi bi-award"></i> Věda</Link></span> 
        </>
    )
}

export const TeacherHeader = (props) => {
    return (
        <Row>
            <Col md={8} >
                {props.label} <TeacherSmall {...props} />
            </Col>
            <Col md={4}>
                <TeacherPageLinks {...props}/>
            </Col>
        </Row>
    )
}

export const TeacherSupervisorPhDActive = (props) => {
    return (
        <Card>
            <Card.Header>
                <Card.Title>
                    Školitel - aktuální práce 
                </Card.Title>
            </Card.Header>
            <Card.Body>

            </Card.Body>
        </Card>

    )
}

export const TeacherSupervisorPhDFinished = (props) => {
    return (
        <Card>
            <Card.Header>
                <Card.Title>
                    Školitel - ukončené práce 
                </Card.Title>
            </Card.Header>
            <Card.Body>

            </Card.Body>
        </Card>
    )
}

export const TeacherSupervisorMscActive = (props) => {
    return (
        <Card>
            <Card.Header>
                <Card.Title>
                    Vedoucí - aktuální práce
                </Card.Title>
            </Card.Header>
            <Card.Body>

            </Card.Body>
        </Card>
    )
}

export const TeacherSupervisorMscFinished = (props) => {
    return (
        <Card>
            <Card.Header>
                <Card.Title>
                    Vedoucí - ukončené práce
                </Card.Title>
            </Card.Header>
            <Card.Body>

            </Card.Body>
        </Card>
    )
}

export const TeacherSupervisor = (props) => {
    return (
        <Card>
            <Card.Header>
                <Card.Title>
                    <TeacherHeader label="Školitel / Vedoucí" {...props} />
                </Card.Title>
            </Card.Header>
            <Card.Body>
                <Row>
                    <Col md={6}>
                        <TeacherSupervisorMscActive {...props} />
                    </Col>
                    <Col md={6}>
                        <TeacherSupervisorPhDActive {...props} />
                    </Col>
                </Row>
                <Row>
                    <Col md={6}>
                        <TeacherSupervisorMscFinished {...props} />
                    </Col>
                    <Col md={6}>
                        <TeacherSupervisorPhDFinished {...props} />
                    </Col>
                </Row>
            </Card.Body>
        </Card>
    )
}

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

export const TeacherGrantSubjectsActual = (props) => {
    return (
        <Card>
            <Card.Header>
                <Card.Title>
                    Garant - Platné předměty
                </Card.Title>
            </Card.Header>
            <Card.Body>

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
                    <TeacherHeader label="Garant" {...props} />
                </Card.Title>
            </Card.Header>
            <Card.Body>
                <Row>
                    <Col md={6}>
                        <TeacherGrantProgramsActual {...props} />
                    </Col>
                    <Col md={6}>
                        <TeacherGrantSubjectsActual {...props} />
                    </Col>
                </Row>
                <Row>
                    <Col md={6}>
                        <TeacherGrantProgramsPast {...props} />
                    </Col>
                    <Col md={6}>
                        <TeacherGrantSubjectsPast {...props} />
                    </Col>
                </Row>
            </Card.Body>
        </Card>
    )
}

export const TeacherTimeTable = (props) => {
    return (
        <Card>
            <Card.Header>
                <Card.Title>
                    <TeacherHeader label="Rozvrh" {...props} />
                </Card.Title>
            </Card.Header>
            <Card.Body>
                <Row>
                    <Col md={12}>
                        <svg style={{"display": "inline-block",	"width": "100%"}} viewBox="0 0 1280 720" preserveAspectRatio="xMinYMid" width="1280" height="720" xmlns="http://www.w3.org/2000/svg" overflow="hidden">
                            <rect x="0" y="0" width="1280" height="720" style={{"fill":"rgb(127,127,127)", "strokeWidth":"3", "stroke": "rgb(0,0,0)"}} />
                            <rect x="50" y="20" width="300" height="100" style={{"fill":"rgb(127,127,255)", "strokeWidth":"3", "stroke": "rgb(0,0,0)"}} />
                        </svg>                    
                    </Col>
                </Row>
            </Card.Body>
        </Card>
    )
}

export const TeacherTasks = (props) => {
    return (
        <Card>
            <Card.Header>
                <Card.Title>
                    <TeacherHeader label="Úkoly" {...props} />
                </Card.Title>
            </Card.Header>
            <Card.Body>
                <Row>
                    <Col md={12}>
                    <table className="table table-striped table-bordered">
                            <thead>
                                <tr>
                                    <td>#</td>
                                    <td>Termín</td>
                                    <td>Zadavatel</td>
                                    <td>Popis</td>
                                    <td>Odkaz</td>
                                    <td>.</td>
                                    <td>Nástroje</td>
                                </tr>
                            </thead>
                            <tbody>
                                <tr>
                                    <td>4523</td>
                                    <td>17.11.2022</td>
                                    <td><TeacherSmall {...props} /></td>
                                    <td>Naplánovat předmět Bezpečnost</td>
                                    <td><a href={""}>Plánování</a></td>
                                    <td>.</td>
                                    <td><a className="btn btn-sm btn-outline-success">Splněno</a></td>
                                </tr>
                                <tr>
                                    <td>4523</td>
                                    <td>17.11.2022</td>
                                    <td><TeacherSmall {...props} /></td>
                                    <td>Naplánovat předmět Bezpečnost</td>
                                    <td><a href={""}>Plánování</a></td>
                                    <td>.</td>
                                    <td><a className="btn btn-sm btn-outline-success">Splněno</a></td>
                                </tr>
                            </tbody>
                        </table>                    
                        </Col>
                </Row>
            </Card.Body>
        </Card>
    )
}

export const TeacherMessages = (props) => {
    return (
        <Card>
            <Card.Header>
                <Card.Title>
                    <TeacherHeader label="Zprávy" {...props} />
                </Card.Title>
            </Card.Header>
            <Card.Body>
                <Row>
                    <Col md={12}>
                    <table className="table table-striped table-bordered">
                            <thead>
                                <tr>
                                    <td>#</td>
                                    <td>Termín</td>
                                    <td>Odesílatel</td>
                                    <td>Popis</td>
                                    <td>Odkaz</td>
                                    <td>.</td>
                                    <td>Nástroje</td>
                                </tr>
                            </thead>
                            <tbody>
                                <tr>
                                    <td>4523</td>
                                    <td>17.11.2022</td>
                                    <td><TeacherSmall {...props} /></td>
                                    <td>Byl aktualizován předpis</td>
                                    <td><a href={""}>Znění</a></td>
                                    <td>.</td>
                                    <td><a className="btn btn-sm btn-outline-success">Odstranit</a></td>
                                </tr>
                                <tr>
                                    <td>4523</td>
                                    <td>17.11.2022</td>
                                    <td><TeacherSmall {...props} /></td>
                                    <td>Byl aktualizován předpis</td>
                                    <td><a href={""}>Znění</a></td>
                                    <td>.</td>
                                    <td><a className="btn btn-sm btn-outline-success">Odstranit</a></td>
                                </tr>
                            </tbody>
                        </table>                    
                        </Col>
                </Row>
            </Card.Body>
        </Card>
    )
}

export const TeacherStudyGroups = (props) => {
    return (
        <Card>
            <Card.Header>
                <Card.Title>
                    <TeacherHeader label="Výuka" {...props} />
                </Card.Title>
            </Card.Header>
            <Card.Body>
                <Row>
                    <Col md={12}>
                        <table className="table table-striped table-bordered">
                            <thead>
                                <tr>
                                    <td>#</td>
                                    <td>VZP</td>
                                    <td>C</td>
                                    <td>.</td>
                                    <td>.</td>
                                    <td>.</td>
                                    <td>Nástroje</td>
                                </tr>
                            </thead>
                            <tbody>
                                <tr>
                                    <td>23-5KB</td>
                                    <td>17</td>
                                    <td>7</td>
                                    <td>.</td>
                                    <td>.</td>
                                    <td>.</td>
                                    <td><a className="btn btn-sm btn-outline-success">Detail</a></td>
                                </tr>
                                <tr>
                                    <td>23-5KB</td>
                                    <td>17</td>
                                    <td>7</td>
                                    <td>.</td>
                                    <td>.</td>
                                    <td>.</td>
                                    <td><a className="btn btn-sm btn-outline-success">Detail</a></td>
                                </tr>
                            </tbody>
                        </table>
                    </Col>
                </Row>
            </Card.Body>
        </Card>
    )
}
/**
 * Retrieves the data from GraphQL API endpoint
 * @param {*} id - identificator
 * @function
 */
 export const UserLargeQuery = (id) => 
 fetch('/gql', {
     method: 'POST',
     headers: {
         'Content-Type': 'application/json',
     },
     cache: 'no-cache', // *default, no-cache, reload, force-cache, only-if-cached
     redirect: 'follow', // manual, *follow, error
     body: JSON.stringify({
         "query":
             `query ($id: UUID!) {
                userById(id: $id) {
                    id
                    name
                    surname
                    email
                    
                    membership {
                      group {
                        id
                        name
                        grouptype {
                          id
                          name
                        }
                      }
                      
                    }
                  }
                }`,
         "variables": {"id": id}
     }),
 })


/**
 * Fetch the data from API endpoint and renders a page representing a department
 * @param {*} props - extra props for encapsulated components / visualisers
 * @param {*} [props.as = DepartmentLargeStoryBook] - ReactJS component (function) which is responsible for rendering
 * @param {*} [props.with = DepartmentLargeQuery] - function fetching the data and returning promise with the data from API endpoint
 * @function
 */
 export const TeacherLargeFetching = (props) => {

    const Visualizer = props.as || TeacherLargeStoryBook;
    const queryFunc = props.with || UserLargeQuery;

    const [state, error] = useQueryGQL(props.id, queryFunc, (response) => response.data.userById, [props.id])
    
    console.log(JSON.stringify(state))

    if (state != null) {
      return <Visualizer {...props} {...state} />
    } else if (error != null) {
        return <LoadingError error={error} />
    } else {
        return <Loading>Uživatel {props.id}</Loading>
    }
}

export const TeacherTimeTablePage = (props) => {
    const { id } = useParams();

    return (
        <TeacherLargeFetching {...props} id={id} as={TeacherTimeTable}/>
    )       
}

export const TeacherPage = (props) => {
    const { id } = useParams();

    return (
        <TeacherLargeFetching {...props} id={id} />
    )       
}


export const TeacherSupervisorPage = (props) => {
    const { id } = useParams();

    return (
        <TeacherLargeFetching {...props} id={id} as={TeacherSupervisor}/>
    )       
}

export const TeacherTasksPage = (props) => {
    const { id } = useParams();

    return (
        <TeacherLargeFetching {...props} id={id} as={TeacherTasks}/>
    )       
}

export const TeacherGrantPage = (props) => {
    const { id } = useParams();

    return (
        <TeacherLargeFetching {...props} id={id} as={TeacherGrant}/>
    )       
}


export const TeacherStudyGroupsPage = (props) => {
    const { id } = useParams();

    return (
        <TeacherLargeFetching {...props} id={id} as={TeacherStudyGroups}/>
    )       
}


export const TeacherMessagesPage = (props) => {
    const { id } = useParams();

    return (
        <TeacherLargeFetching {...props} id={id} as={TeacherMessages}/>
    )       
}
