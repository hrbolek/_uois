const path = require('path')
const fs = require('fs')
const cracoBabelLoader = require('craco-babel-loader')

// manage relative paths to packages
const appDirectory = fs.realpathSync(process.cwd())
const resolvePackage = relativePath => path.resolve(appDirectory, relativePath)

module.exports = {
  plugins: [
    {
      plugin: cracoBabelLoader,
      options: {
        includes: [
          resolvePackage('node_modules/@uoisfrontend/user'),
          resolvePackage('node_modules/@uoisfrontend'),
          resolvePackage('node_modules/uoisfrontend'),
          resolvePackage('@uoisfrontend/user'),
          resolvePackage('user'),
          resolvePackage('@uoisfrontend'),
          resolvePackage('uoisfrontend'),
        ],
      },
    },
  ],
}