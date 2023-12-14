var path = require('path')

const { override, babelInclude } = require('customize-cra')

module.exports = function (config, env) {
  return Object.assign(
    config,
    override(
      babelInclude([
        /* transpile (converting to es5) code in src/ and shared component library */
        path.resolve('src'),
        path.resolve('../../packages/shared'),
        path.resolve('../../packages/user'),
        path.resolve('../../packages/group'),
        path.resolve('../../packages/event'),
        path.resolve('../../packages/survey'),
        path.resolve('../../packages/facility'),
        path.resolve('../../packages/program'),
        path.resolve('../../packages/plan'),
        path.resolve('../../packages/form'),
        path.resolve('../../packages/special'),
      ])
    )(config, env)
  )
}