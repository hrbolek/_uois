import { useParams } from "react-router-dom";
import { useState, useCallback } from "react";
import { GraphiQL } from 'graphiql';

//import { LoginButton } from "../../helpers/index";

export const LoginButton = (props) => <></>

export const ApiPage = (props) => {

    const [parameters, setParameters] = useState({fetchURL: '/api/gql'})

    const updateURL = useCallback(() => null, []);
    const onEditQuery = useCallback(
        (newQuery) => {
            setParameters({...parameters, query: newQuery})
            updateURL();
        }, []
    )

    const onEditVariables = useCallback(
        (newVariables) => {
            setParameters({...parameters, variables: newVariables})
            updateURL();
        }, []
    )

    const onEditOperationName = useCallback(
        (newOperationName) => {
            parameters.operationName = newOperationName;
            setParameters({...parameters, operationName: newOperationName})
            updateURL();
        }, []
    )

    const graphQLFetcher = useCallback(
        (graphQLParams) => {
            // This example expects a GraphQL server at the path /graphql.
            // Change this to point wherever you host your GraphQL server.
            
                console.log('fetching')
                return fetch(parameters.fetchURL, {
                    method: 'post',
                    headers: {
                        'Accept': 'application/json',
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify(graphQLParams),
                }).then(function (response) {
                    return response.text();
                }).then(function (responseBody) {
                    try {
                        const asJSON = JSON.parse(responseBody);
                        console.log('got schema')
                        return asJSON;
                    } catch (error) {
                        return responseBody;
                    }
                });
        }, [parameters.fetchURL]
    )

    return (
        <div style={{height: "100vh", margin: "0",  overflow: "hidden" }}>
        <LoginButton /> <br/>
        <GraphiQL 
            {...parameters}
            fetcher = {graphQLFetcher}
            onEditQuery = {onEditQuery}
            onEditVariables = {onEditVariables}
            onEditOperationName = {onEditOperationName}
        />
        </div>
    )       
}


export const ApiPageNew = (props) => {
    return (
        <div>API</div>
    )
}