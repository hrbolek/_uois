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

import { UserModelPage } from './entities/user/user';
import { GroupModelPage } from './entities/group/group';
import { SubjectPage } from './entities/subject/subject';
import { StudyPlanModelPage } from './entities/studyplan/studyplan'

import { root } from './entities/index'

const Home = (props) => {
  return (
    <Nav>
        <Nav.Link as={Link} to={root + "/"}>Home</Nav.Link>
        <Nav.Link as={Link} to={root + "/users/"}>Uživatelé</Nav.Link>
        <Nav.Link as={Link} to={root + "/groups/"}>Skupiny</Nav.Link>
        <Nav.Link as={Link} to={root + "/subjects/"}>Předměty</Nav.Link>
        <Nav.Link as={Link} to={root + "/studyplans/"}>PSP</Nav.Link>
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
          <Route path={root + "/users/rozvrh/:id"}>
            <UserModelPage rozvrh />
          </Route>

          <Route path={root + "/users/:id"}>
            <UserModelPage />
          </Route>
          <Route path={root + "/groups/:id"}>
            <GroupModelPage />
          </Route>
          <Route path={root + "/subjects/:id"}>
            <SubjectPage />
          </Route>
          <Route path={root + "/studyplans/:id"}>
            <StudyPlanModelPage />
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
