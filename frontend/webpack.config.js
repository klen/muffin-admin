const path = require('path'),
  webpack = require('webpack'),
  mode = process.env.NODE_ENV

module.exports = {
  entry: '.',

  output: {
    filename: 'main.js',
    path: path.resolve(__dirname, '../muffin_admin'),
    publicPath: '/admin',
  },

  module: {
    rules: [
      {
        test: /\.jsx$/,
        use: {
          loader: 'babel-loader',
          options: {
            presets: ['@babel/preset-env', '@babel/preset-react'],
            plugins: ['@babel/plugin-transform-runtime'],
          },
        },
      },
    ],
  },

  plugins: [new webpack.EnvironmentPlugin({ NODE_ENV: 'production' })],

  mode: mode || 'production',
  devtool: mode == 'development' && 'inline-source-map',

  devServer: {
    hot: true,
    open: true,
    proxy: [
      {
        context: ['!*.js'],
        target: 'http://localhost:5000',
      },
    ],
  },
}
