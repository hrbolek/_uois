const { ApolloServer } = require("apollo-server");
const { ApolloGateway } = require("@apollo/gateway");

const gateway = new ApolloGateway({
  serviceList: [
    { name: "usersAndGroups", url: "http://ug_gql:8000" },
  ],
});

const server = new ApolloServer({ gateway });

server.listen().then(({ url }) => {
  console.log(`🚀 Server ready at ${url}`);
});