//const { ApolloServer } = require("apollo-server");
const { ApolloServer } = require("apollo-server-express");

const { ApolloGateway, IntrospectAndCompose, RemoteGraphQLDataSource } = require("@apollo/gateway");

const express = require('express')
//const http = require('http')



const getENV = (name, defaultValue) => {
  console.log(process.env)

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

  const servicesstr = getENV("SERVICES", "[]");
  const subgraphs = JSON.parse(servicesstr)
  console.log(subgraphs)
  if (subgraphs.length === 0) {
      console.log("******************************************************")
      console.log("**            Missing SERVICES env ??               **")
      console.log("******************************************************")
  }

  const gateway = new ApolloGateway({
    supergraphSdl: new IntrospectAndCompose({ subgraphs }),
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
                  console.log('header item: ' + headerItem)
                  console.log('header item type: ' + (typeof headerItem))
                  console.log('header item: ' + JSON.stringify(headerItem))
                  console.log('header item methods: ' + JSON.stringify(Object.keys(headerItem)))
                  if (headerItem[0].startsWith('Authorization')) {
                    const [key, value] = headerItem.split(' ')
                    request.http?.headers.set(key, String(value));
                  }
              }
          }

          //console.log(JSON.stringify(Object.keys(request)))
          //console.log(JSON.stringify(Object.keys(request.http)))
          console.log('request for ', JSON.stringify(request.http.url))
          if (request.query) { console.log(JSON.stringify(request.query)) }
          if (request.variables) { console.log(JSON.stringify(request.variables)) }

          //console.log(JSON.stringify(request.context))
          //console.log(JSON.stringify(typeof context))

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

          request.http.timeout = 5 * 60
        }
      });
    }
  })

  const app = express();
  //const httpServer = http.createServer(app);
  const PORT = getENV("PORT", "3000");

  const server = new ApolloServer({ gateway });

  console.log('server pre start')
  await server.start()
  console.log('server post start')

  server.applyMiddleware({ app, path: '/api/gql' });


  app.listen(PORT, () => {
    console.log(`🚀 Server ready at ${PORT}`);
  });

})()
