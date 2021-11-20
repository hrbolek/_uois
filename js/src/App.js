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

import { Students, StudentLarge, StudentPage } from './entities/student/student';
import { TeacherLarge, TeacherPage } from './entities/teacher/teacher';
import { GroupPage, GroupLarge } from './entities/group/group';
import { SubjectPage } from './entities/subject/subject';

import { root } from './entities/index'

const Home = (props) => {
  return (
    <Nav>
        <Nav.Link as={Link} to={root + "/"}>Home</Nav.Link>
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
          <Route path={root + "/teachers/:id"}>
            <TeacherPage />
          </Route>
          <Route path={root + "/teachers/"}>
            <TeacherLarge />
          </Route>
          <Route path={root + "/students/:id"}>
            <StudentPage />
          </Route> 
          <Route path={root + "/students/"}>
            <Students />
          </Route>
          <Route path={root + "/groups/:id"}>
            <GroupPage />
          </Route>
          <Route path={root + "/subjects/:id"}>
            <SubjectPage />
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
