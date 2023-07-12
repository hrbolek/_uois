import { authorizedFetch } from "./authorizedFetch"
import { UserQuery } from "./UserQuery"
import { EventQuery } from "./EventQuery"

export { CreateFetchQuery, CreateAsyncActionFromIdQuery, CreateAsyncActionFromPageQuery } from "./creators"

const All = { authorizedFetch, UserQuery, EventQuery}
export default All

export { authorizedFetch } from "./authorizedFetch"
export { UserQuery } from "./UserQuery"


// const myJson = require('./queries.json');
// const myString = require('./queries.txt?raw');
// const myString = require('./queries.txt');

// console.log(myJson)
// console.log(myString)