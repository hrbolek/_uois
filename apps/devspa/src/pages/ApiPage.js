import 'graphiql/src/style.css';
import { useState, useCallback, createRef } from "react";
import { GraphiQL } from 'graphiql';
import { useExplorerPlugin } from '@graphiql/plugin-explorer';
import { createGraphiQLFetcher } from "@graphiql/toolkit"
import { useRef } from "react";
import { forwardRef } from "react";

export const ApiPageOld = ({}) => {
    // const graphiql = useRef(null);
    // const [graphiql] = useState(forwardRef(null))
    const [parameters, setParameters] = useState({fetchURL: '/api/gql'})
    const [counter, setCounter] = useState(0)

    // const updateURL = useCallback(() => null, []);
    const updateURL = () => null;
    // const onEditQuery = useCallback(
    //     (newQuery) => {
    //         setParameters({...parameters, query: newQuery})
    //         updateURL();
    //     }, []
    // )
    const onEditQuery = (newQuery) => {
            setParameters({...parameters, query: newQuery})
            updateURL();
        }

    // const onEditVariables = useCallback(
    //     (newVariables) => {
    //         setParameters({...parameters, variables: newVariables})
    //         updateURL();
    //     }, []
    // )
    const onEditVariables = (newVariables) => {
            setParameters({...parameters, variables: newVariables})
            updateURL();
        }

    // const onEditOperationName = useCallback(
    //     (newOperationName) => {
    //         parameters.operationName = newOperationName;
    //         setParameters({...parameters, operationName: newOperationName})
    //         updateURL();
    //     }, []
    // )
    const onEditOperationName = (newOperationName) => {
            parameters.operationName = newOperationName;
            setParameters({...parameters, operationName: newOperationName})
            updateURL();
        }

    // const explorerPlugin = useExplorerPlugin({
    //     query: parameters.query,
    //     onEdit: onEditQuery,
    //   });

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
                }).then((response) => {
                    return response.text();
                }).then( (responseBody) => {
                    // graphiql.current?.refresh()
                    // if (graphiql.current) {
                    //     console.log("graphiql.current?.refresh()")
                    // }
                    setCounter(value => value + 1)
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
    // const graphQLFetcher = (graphQLParams) => {
    //         // This example expects a GraphQL server at the path /graphql.
    //         // Change this to point wherever you host your GraphQL server.

    //             console.log('fetching')
    //             return fetch(parameters.fetchURL, {
    //                 method: 'post',
    //                 headers: {
    //                     'Accept': 'application/json',
    //                     'Content-Type': 'application/json'
    //                 },
    //                 body: JSON.stringify(graphQLParams),
    //             }).then(function (response) {
    //                 return response.text();
    //             }).then(function (responseBody) {
    //                 try {
    //                     const asJSON = JSON.parse(responseBody);
    //                     console.log('got schema')
    //                     return asJSON;
    //                 } catch (error) {
    //                     return responseBody;
    //                 }
    //             });
    //     }

    console.log("render graphiql")
    return (
        // <div style={{height: "100vh"}}>
        <div className='graphiql-container' style={{height: "100vh", margin: "0", display: "flex" }}>
        {/* <div > */}
        
        <GraphiQL 
            {...parameters}
            // plugins= {[explorerPlugin]}
            fetcher = {graphQLFetcher}
            onEditQuery = {onEditQuery}
            onEditVariables = {onEditVariables}
            onEditOperationName = {onEditOperationName}
        />
        </div>
    )
}


export const ApiPage = (props) => {


    const [query, setQuery] = useState("");

    const fetcher = createGraphiQLFetcher({
        url: '/api/gql',
        headers: {}
      });

    // const explorerPlugin = GraphiQLPluginExplorer.useExplorerPlugin({
    //     query: query,
    //     onEdit: setQuery,
    // });
    return (
        <div style={{height: "100vh", margin: "0", display: "flex" }}>
            <GraphiQL 
                fetcher={fetcher} defaultEditorToolsVisibility={true}
                //plugins: [explorerPlugin],
                query={query}
                onEditQuery={setQuery}
                inputValueDeprecation={ true} />
        </div>
    )
    
    


    // return (
    //     <div>API</div>
    // )
}
