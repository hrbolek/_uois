import logo from './logo.svg';
import './App.css';


import {
  BrowserRouter as Router, Routes, Route,
  Outlet, Link, useMatch
} from "react-router-dom";

import 'bootstrap/dist/css/bootstrap.min.css';
import Nav from 'react-bootstrap/Nav';
import Container from 'react-bootstrap/Container';

//import { GroupPage, GroupLarge } from './entities/group/group';
import { SubjectPage } from './entities/studyprogram/subject';

import { TeacherPage } from './entities/person/teacher';
import { StudentPage } from './entities/person/student';
import { DepartmentPage } from './entities/group/department';
import { FacultyPage } from './entities/group/faculty';
import { GroupPage } from './entities/group/group';

import { ArealPage } from './entities/areal/areal';
import { BuildingPage } from './entities/areal/building';
import { RoomPage } from './entities/areal/room';

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


function App() {
/*
*/
  return (
      <Router>
        <Routes>
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

export default App;
