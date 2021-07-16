const path = require('path'), webpack = require('webpack');

module.exports = {
  entry: './frontend.js',
  output: {
    filename: 'main.js',
    path: path.resolve(__dirname, '../muffin_admin'),
  },
  module: {
    rules: [
      {
        test: /\.js$/,
        exclude: /node_modules/,
        use: {
          loader: "babel-loader",
          options: {
            presets: ["@babel/preset-env", "@babel/preset-react"],
            plugins: ["@babel/plugin-transform-runtime"],
          },
        },
      },
    ]
  },

  plugins: [
    new webpack.EnvironmentPlugin({NODE_ENV: 'production'}),
  ],

  mode: process.env.NODE_ENV || "production",
  devtool: process.env.NODE_ENV == "development" && "inline-source-map",
  devServer: {
    hot: true,
    proxy: [{
      context: ['!*.js'],
      target: 'http://localhost:5000',
    }]

  }
};
