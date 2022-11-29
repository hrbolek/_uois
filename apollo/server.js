//const { ApolloServer } = require("apollo-server");
const { ApolloServer } = require("apollo-server-express");

const { ApolloGateway, IntrospectAndCompose } = require("@apollo/gateway");

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
        { name: "workflows", url: "http://gql_workflow:8000/gql" },
        { name: "events", url: "http://gql_events:8000/gql" },
        { name: "events", url: "http://gql_personalities:8000/gql" },

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