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


export function App() {
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

