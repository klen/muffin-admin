const path = require('path'),
  webpack = require('webpack'),
  mode = process.env.NODE_ENV

module.exports = {
  entry: './src/web',

  output: {
    filename: 'main.js',
    path: path.resolve(__dirname, '../muffin_admin'),
    publicPath: '/admin',
  },

  module: {
    rules: [
      {
        test: /\.jsx?$/,
        exclude: /node_modules/,
        use: {
          loader: 'babel-loader',
        },
      },
    ],
  },

  plugins: [new webpack.EnvironmentPlugin({ NODE_ENV: 'production' })],

  mode: mode || 'production',
  devtool: mode == 'development' && 'inline-source-map',

  resolve: {
    extensions: ['.jsx', '.js'],
  },

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
