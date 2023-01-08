import { Link, useParams } from "react-router-dom";
import Card from "react-bootstrap/Card";

import Row from "react-bootstrap/Row";
import Col from "react-bootstrap/Col";

import { root } from '../../helpers/index';
import { useQueryGQL, Loading, LoadingError, authorizedFetch } from '../../helpers/index';

export const TeacherSmall = (props) => {
    console.log(JSON.stringify(props))
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

export const DepartmentSmall = (props) => {
    return (
        <>
        <Link to={root + "/groups/department/" + (props.id)}>{props.name} </Link>
        </>
    )
}

export const FacultySmall = (props) => {
    return (
        <>
        <Link to={root + "/groups/faculty/" + (props.id)}>{props.name} </Link>
        </>
    )
}

export const UniversitySmall = (props) => {
    return (
        <>
        <Link to={root + "/groups/university/" + (props.id)}>{props.name} </Link>
        </>
    )
}

const DictOfComponents = {
    'univerzita': UniversitySmall,
    'fakulta': FacultySmall,
    'katedra': DepartmentSmall
}

export const TeacherMembership = (props) => {
    const { membership } = props
    console.log('TeacherMembership')
    console.log(JSON.stringify(membership))
    return (
            <>
            {membership.map((item, index) => {
                console.log(JSON.stringify(item.group.grouptype))
                const Visualiser = DictOfComponents[item.group?.grouptype?.name]??UniversitySmall
                return (
                    <Row key={item.group.id}>
                        <Col><b>{item.group?.grouptype?.name}</b></Col>
                        <Col><Visualiser {...item.group}/></Col>
                    </Row>
                )
            }
            )}
            </>
    )
}

export const TeacherRoles = (props) => {
    const { roles } = props
    console.log('TeacherRoles')
    console.log(JSON.stringify(TeacherRoles))
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
                    <TeacherSmall {...props}/>
                </Card.Title>
            </Card.Header>
            <Card.Body>
                <Row>
                    <b>Členství</b>
                    <hr />
                </Row>
                <Row>
                    <TeacherMembership {...props}/>
                </Row>
            </Card.Body>
            <Card.Body>
                <Row>
                    <b>Role</b>
                    <hr />
                </Row>
                <Row>
                    <TeacherRoles {...props}/>
                </Row>
            </Card.Body>
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

export const SVGTime = (props) => {
    const { Xdelta, HourValue } = props
    return (
        <>
            <rect x={Xdelta} y="-25" width="180" height="25" stroke="#000000" stroke-width="1" fill="#FFFFFF"></rect>
            <text font-family="Calibri,Calibri_MSFontService,sans-serif" font-weight="600" font-size="18" transform={"translate(" + (Xdelta + 5) +" -10)"}>
                {HourValue}
            </text>
        </>
    )
}

export const SVGDate = (props) => {
    const { YDelta, DateValue, DayValue } = props
    return (
        <>
            <rect x="-60" y={YDelta} width="60" height="100" stroke="#000000" stroke-width="1" fill="#FFFFFF"></rect>
            <text font-family="Calibri,Calibri_MSFontService,sans-serif" font-weight="600" font-size="18" transform={"translate(-58 " + (YDelta + 20) + ")"}>
                {DateValue}
                <tspan font-size="18" font-weight="400" x="-0.0424118" y="23">{DayValue}</tspan>
            </text>
        </>
    )
}

export const SVGEvent = (props) => {
    const { XDelta, YDelta, fillColor, lesson, subject, teacher, room } = props
    return (
        <>
            <rect x={XDelta} y={YDelta} width="180" height="100" stroke="#f7b4b7" stroke-width="1" fill={fillColor}></rect>
            <text font-family="Calibri,Calibri_MSFontService,sans-serif" font-weight="600" font-size="15" transform={"translate(" + (XDelta + 5) + " " + (YDelta + 14) +")"}>
                <a href={"/ui/studyprograms/subject/" + lesson.id} target="_top">{lesson.name}</a>
                <tspan font-size="15" font-weight="400" x="-0.0424118" y="18"><a href={"/ui/studyprograms/subject/" + subject.id} target="_top"></a>{subject.name}</tspan>
                <tspan font-size="15" font-weight="400" x="1.04089" y="38"><a href={"/ui/users/teacher/" + teacher.id} target="_top">{teacher.name + " " + teacher.surname }</a></tspan>
                <tspan font-size="15" font-weight="400" x="1.04089" y="58"><a href={"/ui/areals/room/" + room.id} target="_top">{room.name}</a></tspan>
                <tspan font-size="15" font-weight="400" x="1.04089" y="78"><a href={"/ui/areals/room/" + room.id} target="_top">skupina</a></tspan>
            </text>
        </>
    )
}

export const SVGTimeTable = (props) => {
    //meritko je v ose x jedna minuta         -> 2 body
    //           v ose y jeden den            -> 100 bodu
    //referencnim bodem je cas 8:00 prvni den -> (0, 0)
    return (
        <svg width="100%" height="100%" xmlns="http://www.w3.org/2000/svg" overflow="hidden" viewBox="-61 -26 1400 550">
         <g>
                <SVGTime Xdelta={0} HourValue={"8:00"} />
                <SVGTime Xdelta={220} HourValue={"9:50"} />
                <SVGTime Xdelta={440} HourValue={"11:40"} />
                <SVGTime Xdelta={780} HourValue={"14:30"} />
                <SVGTime Xdelta={1000} HourValue={"16:20"} />
                <SVGTime Xdelta={1200} HourValue={"18:00"} />

                <SVGDate YDelta={0} DateValue={"8.11."} DayValue={"po"}/>
                <SVGDate YDelta={100} DateValue={"9.11."} DayValue={"út"}/>
                <SVGDate YDelta={200} DateValue={"10.11."} DayValue={"st"}/>
                <SVGDate YDelta={300} DateValue={"11.11."} DayValue={"čt"}/>
                <SVGDate YDelta={400} DateValue={"12.11."} DayValue={"pá"}/>

                <SVGEvent XDelta={780} YDelta={300} fillColor={"#f7b4b7"}
                    lesson={{name: "konzultace", id: "1"}} 
                    subject={{name: "", id: "1"}} 
                    teacher={{name: "Michal", surname: "Svoboda", id: "1"}} 
                    room={{name: "", id: "1"}} />
                <SVGEvent XDelta={220} YDelta={100} fillColor={"#b6bd82"}
                    lesson={{name: "Letecké elektronické systémy", id: "1"}} 
                    subject={{name: "3. Syntéza kmitočtu", id: "1"}} 
                    teacher={{name: "Michal", surname: "Svoboda", id: "1"}} 
                    room={{name: "Č1/120", id: "1"}} />
                <SVGEvent XDelta={220} YDelta={400} fillColor={"#b6bd82"}
                    lesson={{name: "Letecké elektronické systémy", id: "1"}} 
                    subject={{name: "3. Syntéza kmitočtu", id: "1"}} 
                    teacher={{name: "Michal", surname: "Svoboda", id: "1"}} 
                    room={{name: "Č1/120", id: "1"}} />
                <SVGEvent XDelta={0} YDelta={300} fillColor={"#859be9"}
                    lesson={{name: "Mentoring studentů 1. ročníku", id: "1"}} 
                    subject={{name: "", id: "1"}} 
                    teacher={{name: "Jana", surname: "Svobodová", id: "1"}} 
                    room={{name: "Č1/120", id: "1"}} />

                
            </g>
        </svg>        
    )
}

export const SheetA4Week = (props) => {
    const { XDelta, YDelta } = props
    const days = [0, 1, 2, 3, 4];
    const dayHeight = 200
    return (
        <>
            <rect x={XDelta} y={YDelta} width="20" height={dayHeight * days.length} stroke="#000000" stroke-width="1" fill="#FFFFFF">
            </rect>
            {days.map((item, index) => 
                <SheetA4WeekDay XDelta={XDelta} YDelta={YDelta + index * dayHeight} DateValue={item}/>
            )}
        </>
    )
}

export const SheetA4WeekDayLesson = (props) => {
    const { XDelta, YDelta, DateValue } = props
    return (
        <>
            <rect x={XDelta} y={YDelta} width="20" height="30" stroke="#000000" stroke-width="1" fill="#FFFFFF"></rect>
            <text font-family="Calibri,Calibri_MSFontService,sans-serif" font-weight="600" font-size="5" transform={"translate(" + (XDelta + 1) + " " + (YDelta + 5) +")"}>
                <a href={"/ui/studyprograms/subject/"} target="_top">Topic</a>
                <tspan font-size="5" font-weight="400" x="0" y="6"><a href={"/ui/studyprograms/subject/"} target="_top"></a>Subject</tspan>
                <tspan font-size="5" font-weight="400" x="0" y="11"><a href={"/ui/users/teacher/"} target="_top">Teachr</a></tspan>
                <tspan font-size="5" font-weight="400" x="0" y="17"><a href={"/ui/areals/room/"} target="_top">Room</a></tspan>
                <tspan font-size="5" font-weight="400" x="0" y="23"><a href={"/ui/areals/room/"} target="_top">Group</a></tspan>
            </text>
        </>

    )
}

export const SheetA4WeekDay = (props) => {
    const { XDelta, YDelta, DateValue } = props
    const hours = [0, 1, 2, 3, 4, 5]
    return (
        <>
        <rect x={XDelta} y={YDelta} width="20" height="20" stroke="#000000" stroke-width="1" fill="#ffcc99"></rect>
        {hours.map((item, index) => <SheetA4WeekDayLesson XDelta={XDelta} YDelta={YDelta + 20 + 30 * index} />)}
        </>
    )
}

export const SheetA4Date = (props) => {
    const { YDelta } = props
    return (
        <rect x="-60" y={YDelta} width="60" height="100" stroke="#000000" stroke-width="1" fill="#FFFFFF"></rect>
    )
}

export const SheetA4TimeTable = (props) => {
    const weeks = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20 ]
    return (
        <svg width="100%" height="100%" xmlns="http://www.w3.org/2000/svg" overflow="hidden" viewBox="-61 -26 500 1400">
         <g>
             <SheetA4Week XDelta={-50} YDelta={0} />
            <SheetA4Week XDelta={-30} YDelta={0} />
             {weeks.map((item, index) => <SheetA4Week XDelta={index * 20} YDelta={0} /> )}
         </g>
        </svg> 
    )
}

//                <SVGTimeTable />

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
                <SVGTimeTable />
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
                        <SheetA4TimeTable />
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
    authorizedFetch('/gql', {
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
                    externalIds {
                        typeName
                        outerId
                    }
                    membership {
                    group {
                        id
                        name
                        grouptype {
                            id
                            name
                            nameEn
                        }
                    }
                    }
                    roles {
                        id
                        roletype {
                            id
                            name
                        }
                        group {
                            id
                            name
                            grouptype {
                                id
                                name
                                nameEn
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
