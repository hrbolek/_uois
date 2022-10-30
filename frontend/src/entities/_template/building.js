import { useQueryGQL, Loading, LoadingError } from "../index";
import Card from "react-bootstrap/Card";
import { Link, useParams } from "react-router-dom";

import { ArealSmall } from "../areal/areal";
import { TeacherSmall } from "../person/teacher";
import { root } from "../index";
import React from "react";

const buildingRoot = root + '/areals/building';

/**
 * Render link to the Building entity
 * @param {*} props 
 * @param {*} props.id - id of the Building entity
 * @param {string} props.name - the Building's name
 * @returns 
 */
export const BuildingSmall = (props) => {
    return <Link to={buildingRoot + `${props.id}`}>{props.name}{props.children}</Link>
}

/**
 * 
 * @param {*} props 
 * @param {*} props.id - building's id
 * @param {string} props.name - building's name
 * @param {*} props.areal - data describing the areal where the building is located
 * @param {*} props.user - user responsible for the building
 * @param {*[]} props.rooms - rooms in the building 
 * @returns 
 */
export const BuildingMedium = (props) => {
    return (
        <Card>
            <Card.Header>
                Budova {props.name} ({props.id}) Areál <ArealSmall {...props.areal} /> Odpovědná osoba <TeacherSmall {...props.user} />
            </Card.Header>
            <Card.Body>
                {JSON.stringify(props)}
            </Card.Body>
        </Card>
    )
}

/**
 * 
 * @param {*} props - data describing the Building entity
 * @param {*[]} props.rooms - array containgin the rooms
 * @returns {React.Component}
 */
export const BuildingRooms = (props) => {
    return (
        <>
        {props.rooms.map((room, index) => (
            <>
                Učebna {room.name} ({room.id}) <br />
            </>
        ))}
        </>
    )
}

/**
 * 
 * @param {*} props - data describing the Building entity
 * @param {*} props.name - building's name
 * @param {*} props.id - building's id
 * @param {*} props.areal - data describing the areal where the building is located
 * @param {*} props.user - user responsible for the building
 * @param {*[]} props.rooms - rooms in the building
 * @returns {React.Component}
 */
export const BuildingLarge = (props) => {
    return (
        <Card>
            <Card.Header>
                Budova {props.name} ({props.id}) Areál <ArealSmall {...props.areal} /> Odpovědná osoba <TeacherSmall {...props.user} />
            </Card.Header>
            <Card.Body>
                <BuildingRooms {...props} />
            </Card.Body>
            <Card.Body>
                {JSON.stringify(props)}
            </Card.Body>
        </Card>
    )
}

/**
 * Renders Building page with predefined data. 
 * @param {*} props - data to be displayed, overrides predefined data
 * @param {*} props.name - building's name
 * @param {*} props.id - building's id
 * @param {*} props.areal - data describing the areal where the building is located
 * @param {*} props.user - user responsible for the building
 * @param {*[]} props.rooms - rooms in the building
 */
export const BuildingLargeStoryBook = (props) => {
    const extraProps = {
        'id' : 789,
        'name' : 'KŠ/9A',
        'rooms' : [
            {'id': 789, 'name': 'KŠ/9A/586'}
        ],
        'areal' : {'id' : 789, 'name': 'KŠ'},
        'user' : {'id' : 789, 'name': 'John', 'surname': 'Nowick'}
    }
    return <BuildingLarge {...extraProps} {...props} />
}

/**
 * Large Query fetching data from GraphQLAPI
 * @param {*} id - identificator of Building entity
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
                    building(id: ${id}) {
                      id
                      name
                      areal {
                          id
                          name
                      }
                      rooms {
                        id
                        name                        
                      }
                      user {
                        id
                        name
                        surname
                      }
                    }
                  }
            `
        }),
    })

/**
 * Loads data from remote endpoint and renders the page for Building entity
 * @param {id} props.id - id of building entity
 * @param {React.Component} [props.as=BuildingLargeStoryBook] - a ReactJS component responsible for page rendering
 * @param {*} [props.with=BuildingLargeQuery] - function returning Promise 
 * @param {any} props - extra properties for rendering
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
        return <Loading>Nahrávám informace o budově {props.id}</Loading>
    }
}

/**
 * Render the page for Building
 * @param {id} props.id - id of building entity
 * @param {any} props - extra props for page
 */
export const BuildingPage = (props) => {
    const { id } = useParams();

    return <BuildingLargeStoryBook {...props} id={id} />;

}