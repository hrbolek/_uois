import { useEffect, useState, useMemo } from "react";

import Card from "react-bootstrap/Card";
import Row from "react-bootstrap/Row";
import Col from "react-bootstrap/Col";
import { authorizedFetch } from '../../helpers/index';

export const CheckGroupExists = (id) => {
    authorizedFetch('/gql', {
        body: JSON.stringify({
            query: `
            query ($id: UUID!) {
                groupById(id: $id) {
                    id
                }
            }`,
            variables: {id: id}        
        })
    })
    .then(response => response.json()) //convert response into json format
    .then(jsonData => jsonData.data.groupById.id === id) //check if response id is the proper one, if not, group does not exists
}

export const AddGroup = (groupRecord) => {
    authorizedFetch('/gql', {
        body: JSON.stringify({
            query: `
            query ($id: UUID!) {
                groupById(id: $id) {
                    id
                }
            }`,
            variables: {id: groupRecord.id}        
        })
    })
}

export const ImportUG = (jsonData) => {
    const { groups, users, memberships } = jsonData;

    for(let group in groups) {

    }

}

export const ImportPage = (props) => {

    const [json, setJson] = useState({})

    const openFile = (event) => {
        
        const inputFiles = event.target.files;
        
        const reader = new FileReader();
        reader.onload = () => {
          const text = reader.result;
          const jsonObj = JSON.parse(text)
          setJson(jsonObj);
        };
        reader.readAsText(inputFiles[0]);
    }

    return (
        <Card>
            <Card.Header>
                Importy
            </Card.Header>
            <Card.Body>

                <Card>
                    <Card.Header>
                        Skupiny a uživatelé
                    </Card.Header>
                    <Card.Body>

                        <form className="row">
                            <div className="mb-3">
                                <label htmlFor="fileInput" className="form-label">Soubor typu JSON</label>
                                <input id="fileInput" className="form-control" type="file" placeholder="Default input" aria-label="default input example" onChange={openFile}/>
                            </div>
                            <div className="mb-3">
                                <label htmlFor="textOutput" className="form-label">JSON data</label>
                                <div id="textOutput">
                                    {JSON.stringify(Object.keys(json))}<br />
                                    {JSON.stringify(json.groups[0])}
                                </div>
                            </div>
                        </form>
                    </Card.Body>
                </Card>
                <Card>
                    <Card.Header>
                        Areály a budovy
                    </Card.Header>
                    <Card.Body>

                    </Card.Body>
                </Card>
                <Card>
                    <Card.Header>
                        Akreditované programy a předměty
                    </Card.Header>
                    <Card.Body>

                    </Card.Body>
                </Card>
            </Card.Body>
        </Card>
    )
}
