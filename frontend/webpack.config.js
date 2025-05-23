const path = require("path"),
  webpack = require("webpack"),
  mode = process.env.NODE_ENV

module.exports = {
  entry: "./src/web.ts",

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
      {
        test: /\.s?css$/,
        use: [
          "style-loader",
          "css-loader"
        ]
      }
    ],
  },

  plugins: [
    new webpack.EnvironmentPlugin({ NODE_ENV: "production" }),
  ],

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
        target: "http://127.0.0.1:5555",
      },
    ],
  },
}
