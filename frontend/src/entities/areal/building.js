import { useQueryGQL, Loading, LoadingError } from "../index";
import Card from "react-bootstrap/Card";
import Row from "react-bootstrap/Row";
import Col from "react-bootstrap/Col";
import { Link, useParams } from "react-router-dom";

import { root } from "../index";
import { ArealSmall } from "./areal";
import { TeacherMedium } from "../person/teacher";


/** @module Building */

const buildingRoot = root + '/areals/building';

export const BuildingSmall = (props) => {
    return <Link to={buildingRoot + `/${props.id}`}>{props.name}{props.children}</Link>
}

export const BuildingMedium = (props) => {
    return (
        <Card>
            <Card.Header>
                Budova
            </Card.Header>
            <Card.Body>
                {JSON.stringify(props)}
            </Card.Body>
        </Card>
    )
}


export const BuildingRoomList = (props) => {
    return (
        <Card>
            <Card.Header>
                <Card.Title>
                Místnosti
                </Card.Title>
            </Card.Header>
            <Card.Body>
                {JSON.stringify(props)}
            </Card.Body>
        </Card>
    )
}

export const BuildingSpravce = (props) => {
    const spravceProps = {
        'id': 1,
        'name': 'Petr Jana',
        'surname': 'Novak',
        'email': 'petr.jana.novak@uni.world'
    }
    return (
        <TeacherMedium label='Správce' {...spravceProps}/>
    )
}

export const BuildingLarge = (props) => {
    return (
        <Card>
            <Card.Header>
                <Card.Title>
                {props.name} (<ArealSmall {...props.areal}/>)
                </Card.Title>
            </Card.Header>
            <Card.Body>
                <Row>
                    <Col md={3}>
                        <BuildingSpravce {...props}/>
                    </Col>
                    <Col>
                        <BuildingRoomList {...props}/>
                    </Col>
                </Row>
                
            </Card.Body>
        </Card>
    )
}

/**
 * Renders a page with data representing a building, contains predefined data which can are overrided by props
 * @param {*} props 
 * @param {*} props.id - identification
 * @param {string} props.name - name
 * @function
 */
export const BuildingLargeStoryBook = (props) => {
    const extraProps = {
        'id' : 1,
        'name' : 'KŠ/9A',
        'rooms' : [
            {'id': 1, 'name': 'KŠ/9A/586'},
            {'id': 2, 'name': 'KŠ/9A/584'},
            {'id': 3, 'name': 'KŠ/9A/583'},
            {'id': 4, 'name': 'KŠ/9A/588'},
            {'id': 5, 'name': 'KŠ/9A/589'},
        ],
        'areal' : {'id' : 1, 'name': 'KŠ'},
        'user' : {'id' : 1, 'name': 'John', 'surname': 'Nowick'}
    }

   
    return <BuildingLarge {...extraProps} {...props} />
}

/**
 * Retrieves the data from GraphQL API endpoint
 * @param {*} id - identificator
 * @function
 */
export const BuildingLargeQuery = (id) => 
    fetch('/gql', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        cache: 'no-cache', // *default, no-cache, reload, force-cache, only-if-cached
        redirect: 'follow', // manual, *follow, error
        body: JSON.stringify({
            "query":
                `
                query {
                    building(id:${id}) {
                      id
                      name
                      
                      rooms {
                        id
                        name
                      }
                      
                      areal: area {
                        id
                        name
                      }
                    }
                  }
            `
        }),
    })

/**
 * Fetch the data from API endpoint and renders a page representing a building
 * @param {*} props - extra props for encapsulated components / visualisers
 * @param {*} [props.as = BuildingLargeStoryBook] - ReactJS component (function) which is responsible for rendering
 * @param {*} [props.with = BuildingLargeQuery] - function fetching the data and returning promise with the data from API endpoint
 * @function
 */
export const BuildingFetching = (props) => {

    const Visualizer = props.as || BuildingLargeStoryBook;
    const queryFunc = props.with || BuildingLargeQuery;

    const [state, error] = useQueryGQL(props.id, queryFunc, (response) => response.data.building, [props.id])
    
    if (error != null) {
        return <LoadingError error={error} />
    } else if (state != null) {
        return <Visualizer {...props} {...state} />
    } else {
        return <Loading>Budova {props.id}</Loading>
    }
}

export const BuildingPage = (props) => {
    const { id } = useParams();

    return <BuildingFetching {...props} id={id} />;

}