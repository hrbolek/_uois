//const { ApolloServer } = require("apollo-server");
const { ApolloServer } = require("apollo-server-express");

const { ApolloGateway, IntrospectAndCompose, RemoteGraphQLDataSource } = require("@apollo/gateway");

const express = require('express')
//const http = require('http')



const getENV = (name, defaultValue) => {
  const value = process.env[name];

  if (typeof value === "undefined") {
    if (typeof defaultValue === "undefined") {
      throw new Error(`Missing environment varialbe '${name}'`);
    }
    return defaultValue;
  }

  return value;
};

(async function startApolloServer() {
  const gateway = new ApolloGateway({
    supergraphSdl: new IntrospectAndCompose({
      subgraphs: [
        { name: "usersAndGroups", url: "http://gql_ug:8000/gql" },
       // { name: "workflows", url: "http://gql_workflow:8000/gql" },
        { name: "events", url: "http://gql_events:8000/gql" },

        /* 
        * ###########################################################################################################################
        *
        * sem vlozte odkazy na svuj endpoint
        * 
        * ###########################################################################################################################
        */

          // List of federation-capable GraphQL endpoints...
      ],
    }),
    /*
    context: ({ req }) => {
      // toto zjevne neni volano v prubehu dotazu
      console.log('called context function')
      return {
        serverRequest: req,
      };
    },
    //*/
    buildService({ name, url }) {
      return new RemoteGraphQLDataSource({
        url,
        willSendRequest(params) {
          //*
          const { request, context, incomingRequestContext } = params
          console.log('params')
          console.log(JSON.stringify(Object.keys(params)))
          console.log('context')
          console.log(JSON.stringify(Object.keys(context)))

          if (incomingRequestContext) {
              console.log('incomingRequestContext')
              console.log(JSON.stringify(Object.keys(incomingRequestContext)))

              const incRequest = incomingRequestContext.request
              console.log(JSON.stringify(Object.keys(incRequest)))

              const headers = incRequest.http.headers
              const authHeaderValue = headers.get('Authorization')
              console.log('authHeaderValue: ' + authHeaderValue)
              for (const headerItem of headers) {
                  //toto funguje
                  console.log('header: ' + headerItem)
                  if (headerItem.startsWith('Authorization')) {
                    const [key, value] = headerItem.split(' ')
                    request.http?.headers.set(key, String(value));
                  }
              }  
          }
          console.log('request')
          console.log(JSON.stringify(Object.keys(request)))
          console.log(JSON.stringify(Object.keys(request.http)))
          console.log(JSON.stringify(request.query))
          console.log(JSON.stringify(typeof context))
          //const headers = context.req.headers
          /*
          for (const key in headers) {
              const value = headers[key];
              if (value) {
                  request.http?.headers.set(key, String(value));
              }
          }  
          //request.http.headers.set("Authorization", "Bearer ABCDE");
          //*/
        }
      });
    }
  })

  const app = express();
  //const httpServer = http.createServer(app);
  
  const server = new ApolloServer({ gateway });

  await server.start()

  server.applyMiddleware({ app, path: '/gql' });

  const PORT = getENV("PORT", "3000");

  app.listen(PORT, () => {
    console.log(`🚀 Server ready at ${PORT}`);
  });

})()