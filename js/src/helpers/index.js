import {
    Switch,
    Route,
    Link,
    useRouteMatch
  } from "react-router-dom";

import Nav from 'react-bootstrap/Nav';
import { useState } from "react";
import { Button } from "bootstrap";

/*
const SublinksData = [
    {'url': '/timetable/', 'label': 'Rozvrh', 'subComponent': StudentTimeTable},
    {'url': '/group/', 'label': 'Skupina', 'subComponent': StudentGroup},
    {'url': '/teachers/', 'label': 'Učitelé', 'subComponent': StudentTeachers},
    {'url': '/subjects/', 'label': 'Předměty', 'subComponent': StudentSubjects},
];
*/

export const createSubLinks = (descriptor) => 
    (props) => {
        const { url } = useRouteMatch();    
        const links = descriptor.map((item, index) => (<Nav.Link key={index} as={Link} to={`${url}${item.url}`}>{`${item.label}`}</Nav.Link>))
        return (
            <Nav>{links}</Nav>
        )
    };

export const createSwitch = (descriptor) => 
    (props) => {
        const { url } = useRouteMatch();    
        const routes = descriptor.map((item, index) => {
            const SubComponent = item.subComponent;
            return (<Route key={index} path={`${url}${item.url}`}><SubComponent {...props} /></Route>);
        })
        return (
            <Switch>
                {routes}
            </Switch>
        )

    };

/*
export const CreateExpandable = (SmallComponent, MediumComponent) =>
{
    return (props) => {
        const [expanded, setExpanded] = useState(false)
        var result = (<>Error</>)
        if (expanded) {
            result = (
                <>
                    <Button size='sm' onClick={() => setExpanded(false)}>x</Button>
                    <MediumComponent {...props} />
                </>
            )
        } else {
            result = (
                <>
                    <SmallComponent {...props} /><Button size='sm' onClick={() => setExpanded(true)}>více</Button>
                </>
            )
        }
        return result
    }
}
*/