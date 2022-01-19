import { useQueryGQL, Loading, LoadingError } from "../index";
import Card from "react-bootstrap/Card";
import { Link, useParams } from "react-router-dom";

import { ArealSmall } from "../areal/areal";
import { TeacherSmall } from "../person/teacher";
import { root } from "../index";

const buildingRoot = root + '/areals/building';

export const BuildingSmall = (props) => {
    return <Link to={buildingRoot + `${props.id}`}>{props.name}{props.children}</Link>
}

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

export const BuildingFetching = (props) => {
    const [state, error] = useQueryGQL(props.id, BuildingLargeQuery, (response) => response.data.building, [props.id])
    
    if (error != null) {
        return <LoadingError error={error} />
    } else if (state != null) {
        return <BuildingLargeStoryBook {...state} />
    } else {
        return <Loading>Nahrávám informace o budově {props.id}</Loading>
    }
}

export const _BuildingPage = (props) => {
    const { id } = useParams();

    return <BuildingFetching {...props} id={id} />;

}

export const BuildingPage = (props) => {
    const { id } = useParams();

    return <BuildingLargeStoryBook {...props} id={id} />;

}