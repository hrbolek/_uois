const path = require("path")

module.exports = {
    mode: "production",
    entry: {
        index: { import: "./src/index.js" }
    },
    module: {
        rules: [
            {
                test: /\.js?$/,
                exclude: /node_modules/,
                loader: "babel-loader",
            },
        ],
    },
    output: {
        filename: "./dist/index.webpack.js",
        library: 'user',
        //libraryTarget: 'es5',
        libraryTarget: 'amd',
        //clean: true
    },
}