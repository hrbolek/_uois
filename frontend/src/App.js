import logo from './logo.svg';
import './App.css';

import { root } from './helpers/index';

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

import { ApiPage } from './pages/api/api';
import { DepartmentPage } from './pages/group/department';
import { IncommingLogin } from './helpers/index';

const WithLayout = (props) => {
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
    <WithLayout />
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
            <Route path={root + "/api"} element={<ApiPage />}>
            </Route>
            <Route path={root + "/groups/"} element={<WithLayout />}>
              <Route index element={<WithLayout />} />
              <Route path={`department/:id`} element={<DepartmentPage />} />
            </Route>
            <Route path={root + "/login"} element={<IncommingLogin />}>
            </Route>
           
          </Routes>
      
      </Router>
       );
  }

