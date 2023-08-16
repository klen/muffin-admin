const path = require("path"),
  webpack = require("webpack"),
  mode = process.env.NODE_ENV

module.exports = {
  entry: "./src/index.tsx",

  output: {
    filename: "main.js",
    path: path.resolve(__dirname, "../muffin_admin"),
    publicPath: "/admin",
  },

  module: {
    rules: [
      {
        test: /\.tsx?$/,
        use: "ts-loader",
        exclude: /node_modules/,
      },
    ],
  },

  plugins: [new webpack.EnvironmentPlugin({ NODE_ENV: "production" })],

  mode: mode || "production",
  devtool: mode == "development" && "inline-source-map",

  resolve: {
    extensions: [".js", ".tsx", ".ts"],
  },

  devServer: {
    hot: true,
    open: true,
    proxy: [
      {
        context: ["!*.js"],
        target: "http://localhost:5555",
      },
    ],
  },
}
