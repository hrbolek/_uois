import logo from './logo.svg';
import './App.css';


import {
  BrowserRouter as Router,
  Switch,
  Route,
  Link
} from "react-router-dom";

import 'bootstrap/dist/css/bootstrap.min.css';
import Nav from 'react-bootstrap/Nav';
import Container from 'react-bootstrap/Container';

import { UserPage } from './entities/user/user';
//import { GroupPage, GroupLarge } from './entities/group/group';
import { SubjectPage } from './entities/subject/subject';

import { TeacherPage } from './entities/person/teacher';
import { StudentPage } from './entities/person/student';
import { DepartmentPage } from './entities/group/department';
import { FacultyPage } from './entities/group/faculty';
import { GroupPage } from './entities/group/group';

import { ArealPage } from './entities/areal/areal';

import { SubjectSemesterTopicPage } from './entities/studyprogram/lesson';
import { StudyProgramPage } from './entities/studyprogram/studyprogram';

import { root } from './entities/index'

const Home = (props) => {
  return (
    <Nav>
        <Nav.Link as={Link} to={root + "/"}>Home</Nav.Link>
        <Nav.Link as={Link} to={root + "/users/"}>Uživatelé</Nav.Link>
        <Nav.Link as={Link} to={root + "/students/"}>Studenti</Nav.Link>
        <Nav.Link as={Link} to={root + "/teachers/"}>Učitelé</Nav.Link>
        <Nav.Link as={Link} to={root + "/groups/"}>Skupiny</Nav.Link>
        <Nav.Link as={Link} to={root + "/subjects/"}>Předměty</Nav.Link>
    </Nav>

  )
}
function App() {
/*
*/

  return (
    <Router>
      <Container fluid>
        <Home />

        {/* A <Switch> looks through its children <Route>s and
            renders the first one that matches the current URL. */}
        <Switch>
          <Route path={root + "/users/teacher/:id"}>
            <TeacherPage />
          </Route>
          <Route path={root + "/users/student/:id"}>
            <StudentPage />
          </Route>
          <Route path={root + "/groups/department/:id"}>
            <DepartmentPage />
          </Route>
          <Route path={root + "/groups/faculty/:id"}>
            <FacultyPage />
          </Route>
          <Route path={root + "/groups/group/:id"}>
            <GroupPage />
          </Route>

          <Route path={root + "/areals/areal/:id"}>
            <ArealPage />
          </Route>

          <Route path={root + "/studyprograms/program/:id"}>
            <StudyProgramPage />
          </Route>
          <Route path={root + "/studyprograms/lesson/:id"}>
            <SubjectSemesterTopicPage />
          </Route>
          

          <Route path={root + "/users/:id"}>
            <UserPage />
          </Route>

          {/*
          <Route path="/">
            <Home />
          </Route>
          */}
        </Switch>
      </Container>
    </Router>  );
}

export default App;
