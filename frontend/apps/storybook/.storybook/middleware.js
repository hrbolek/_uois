// const proxy = require('http-proxy-middleware')

// module.exports = function expressMiddleware (router) {
//     router.use('/api', proxy({
//         target: 'http://localhost:31180/',
//         changeOrigin: true
//     }))
// }

const { createProxyMiddleware } = require('http-proxy-middleware'); 
module.exports = function(app) { 
    app.use( '/api/gql', 
        createProxyMiddleware({ target: 'http://localhost:31180', changeOrigin: true, }) 
    ); 
};