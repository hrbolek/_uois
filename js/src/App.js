import logo from './logo.svg';
import './App.css';


import {
  BrowserRouter as Router, Routes, Route,
  Outlet, Link, useMatch
} from "react-router-dom";

import 'bootstrap/dist/css/bootstrap.min.css';
import Nav from 'react-bootstrap/Nav';
import Container from 'react-bootstrap/Container';
import Card from 'react-bootstrap/Card';
import Row from 'react-bootstrap/Row';
import Col from 'react-bootstrap/Col';


//import { GroupPage, GroupLarge } from './entities/group/group';
import { SubjectPage, SubjectLargeStoryBook } from './entities/studyprogram/subject';

import { TeacherPage, TeacherLargeStoryBook } from './entities/person/teacher';
import { StudentPage, StudentLargeStoryBook } from './entities/person/student';
import { DepartmentPage, DepartmentLargeStoryBook } from './entities/group/department';
import { FacultyPage, FacultyLargeStoryBook } from './entities/group/faculty';
import { GroupPage, GroupLargeStoryBook } from './entities/group/group';

import { ArealPage, ArealLargeStoryBook } from './entities/areal/areal';
import { BuildingPage, BuildingLargeStoryBook } from './entities/areal/building';
import { RoomPage, RoomLargeStoryBook } from './entities/areal/room';

import { SubjectSemesterTopicPage } from './entities/studyprogram/lesson';
import { StudyProgramPage } from './entities/studyprogram/studyprogram';

import { root } from './entities/index'
import { TimeTablePage, TimeTableA4Page } from './entities/timetable/timetable';

const AppLayout = (props) => {
  return (
    <Container fluid>
    <Nav>
        <Nav.Link as={Link} to={root + "/"}>Home</Nav.Link>
        <Nav.Link as={Link} to={root + "/users/"}>Uživatelé</Nav.Link>
        <Nav.Link as={Link} to={root + "/students/"}>Studenti</Nav.Link>
        <Nav.Link as={Link} to={root + "/teachers/"}>Učitelé</Nav.Link>
        <Nav.Link as={Link} to={root + "/groups/"}>Skupiny</Nav.Link>
        <Nav.Link as={Link} to={root + "/subjects/"}>Předměty</Nav.Link>
    </Nav>
    <Outlet />
    </Container>
  )
}

const Links = (props) => {
  return (
    <>
    <AppLayout />
      <Card>
        <Card.Header>
          <Card.Title>
          Rozcestník na modely stránek
          </Card.Title>
        </Card.Header>
        <Card.Body>
          <Row>
            <Col>
          <Card md={3}>
            <Card.Header>
              <Card.Title>Uživatelé</Card.Title>
            </Card.Header>
            <Card.Body>
              <Link to={root + '/users/student/1'}>Student</Link> <br/>
              <Link to={root + '/users/teacher/1'}>Učitel</Link> <br/>
            </Card.Body>
          </Card>
          </Col>
          <Col>
          <Card md={3}>
            <Card.Header>
              <Card.Title>Skupiny</Card.Title>
            </Card.Header>
            <Card.Body>
              <Link to={root + '/groups/faculty/1'}>Fakulta</Link> <br/>
              <Link to={root + '/groups/department/1'}>Katedra</Link> <br/>
              <Link to={root + '/groups/group/1'}>Studijní skupina</Link> <br/>
            </Card.Body>
          </Card>
          </Col>
          <Col md={3}>
          <Card>
            <Card.Header>
              <Card.Title>
              Budovy
              </Card.Title>
            </Card.Header>
            <Card.Body>
            <Link to={root + '/areals/areal/1'}>Areál</Link> <br/>
              <Link to={root + '/areals/building/1'}>Budova</Link> <br/>
              <Link to={root + '/areals/room/1'}>Učebna</Link> <br/>
            </Card.Body>
          </Card>
          </Col>
          <Col md={3}>
          <Card>
            <Card.Header>
              <Card.Title>
              Akreditace
              </Card.Title>
            </Card.Header>
            <Card.Body>
            <Link to={root + '/studyprograms/program/1'}>Program</Link> <br/>
              <Link to={root + '/studyprograms/subject/1'}>Předmět</Link> <br/>
              <Link to={root + '/studyprograms/lesson/1'}>Lekce</Link> <br/>
            </Card.Body>
          </Card>
          </Col>
          </Row>
          
          <Row>
          <Col>
            <a href="https://github.com/hrbolek/_uois">Git</a>
          </Col>
          </Row>
        </Card.Body>
      </Card>
    </>
  )
}

export function App() {
/*
*/
  return (
      <Router>
        <Routes>
          <Route path={root + "/"} element={<Links />} /> 
          <Route path={root + "/users/"} element={<AppLayout />}>
            <Route index element={<AppLayout />} />
            <Route path={`teacher/:id`} element={<TeacherPage />} />
            <Route path={`student/:id`} element= {<StudentPage />} />
          </Route>
          <Route path={root + "/groups/"} element={<AppLayout />}>
            <Route index element={<AppLayout />} />
            <Route path={`faculty/:id`} element={<FacultyPage />} />
            <Route path={`department/:id`} element={<DepartmentPage />} />
            <Route path={`group/:id`} element={<GroupPage />} />
          </Route>

          <Route path={root + "/areals/"} element={<AppLayout />}>
            <Route index element={<AppLayout />} />
            <Route path={`areal/:id`} element={<ArealPage />} />
            <Route path={`building/:id`} element={<BuildingPage />} />
            <Route path={`room/:id`} element={<RoomPage />} />
          </Route>

          <Route path={root + "/studyprograms/"} element={<AppLayout />}>
            <Route index element={<AppLayout />} />
            <Route path={`program/:id`} element={<StudyProgramPage />} />
            <Route path={`subject/:id`} element={<SubjectPage />} />
            <Route path={`lesson/:id`} element={<SubjectSemesterTopicPage />} />
          </Route>

          <Route path={root + '/A4/:entity/:id/'} >
            <Route index element={<TimeTableA4Page />} />
          </Route>

          <Route path={root + '/svg/:entity/:id/'} >
            <Route index element={<TimeTablePage />} />
          </Route>

        </Routes>
    
    </Router>
     );
}

export function AppDemo() {
  /*
  */
    return (
        <Router>
          <Routes>
            <Route path={root + "/users/"} element={<AppLayout />}>
              <Route index element={<AppLayout />} />
              <Route path={`teacher/:id`} element={<TeacherLargeStoryBook />} />
              <Route path={`student/:id`} element= {<StudentLargeStoryBook />} />
            </Route>
            <Route path={root + "/groups/"} element={<AppLayout />}>
              <Route index element={<AppLayout />} />
              <Route path={`faculty/:id`} element={<FacultyLargeStoryBook />} />
              <Route path={`department/:id`} element={<DepartmentLargeStoryBook />} />
              <Route path={`group/:id`} element={<GroupLargeStoryBook />} />
            </Route>
  
            <Route path={root + "/areals/"} element={<AppLayout />}>
              <Route index element={<AppLayout />} />
              <Route path={`areal/:id`} element={<ArealLargeStoryBook />} />
              <Route path={`building/:id`} element={<BuildingLargeStoryBook />} />
              <Route path={`room/:id`} element={<RoomLargeStoryBook />} />
            </Route>
  
            <Route path={root + "/studyprograms/"} element={<AppLayout />}>
              <Route index element={<AppLayout />} />
              <Route path={`program/:id`} element={<StudyProgramPage />} />
              <Route path={`subject/:id`} element={<SubjectPage />} />
              <Route path={`lesson/:id`} element={<SubjectSemesterTopicPage />} />
            </Route>
  
            <Route path={root + '/A4/:entity/:id/'} >
              <Route index element={<TimeTableA4Page />} />
            </Route>
  
            <Route path={root + '/svg/:entity/:id/'} >
              <Route index element={<TimeTablePage />} />
            </Route>
  
          </Routes>
      
      </Router>
       );
  }

