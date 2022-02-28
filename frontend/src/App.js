import './App.css';


import {
  BrowserRouter as Router, Routes, Route,
  Outlet, Link
} from "react-router-dom";

import 'bootstrap/dist/css/bootstrap.min.css';
import Nav from 'react-bootstrap/Nav';
import Container from 'react-bootstrap/Container';
import Card from 'react-bootstrap/Card';
import Row from 'react-bootstrap/Row';
import Col from 'react-bootstrap/Col';



import { BuildingPage } from './entities/_template/building';
import { root } from './entities/index'

const AppLayout = (props) => {
  return (
    <Container fluid>
    <Nav>
        <Nav.Link as={Link} to={root + "/"}>Home</Nav.Link>
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
            </Card.Body>
          </Card>
          </Col>
          <Col>
          <Card md={3}>
            <Card.Header>
              <Card.Title>Skupiny</Card.Title>
            </Card.Header>
            <Card.Body>
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
              <Link to={root + '/areals/building/1'}>Budova</Link> <br/>
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

          <Route path={root + "/areals/"} element={<AppLayout />}>
            <Route index element={<AppLayout />} />
            <Route path={`building/:id`} element={<BuildingPage />} />
          </Route>
        </Routes>
    
    </Router>
     );
}