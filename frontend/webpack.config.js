const path = require("node:path"),
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
        loader: "esbuild-loader",
        options: {
          loader: "tsx",
          target: "es2015",
        },
        exclude: /node_modules/,
      },
      {
        test: /\.s?css$/,
        use: ["style-loader", "css-loader"],
      },
    ],
  },

  plugins: [new webpack.EnvironmentPlugin({ NODE_ENV: "production" })],

  // react-datepicker 9 uses a dynamic require for the optional date-fns-tz
  ignoreWarnings: [{ module: /react-datepicker/, message: /Critical dependency/ }],

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
