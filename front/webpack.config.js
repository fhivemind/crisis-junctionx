const path = require('path');
const CopyWebpackPlugin = require('copy-webpack-plugin');

module.exports = {
  entry: ['./app/javascripts/app.js'],
  output: {
    path: path.resolve(__dirname, 'build'),
    filename: 'app.js',
  },
  plugins: [
    new CopyWebpackPlugin([
      { from: './app/index.html', to: "index.html" },
      { from: './app/list-item.html', to: "list-item.html" },
      { from: './app/product.html', to: "product.html" },
      { from: './app/user-items.html', to: "user-items.html" },
      { from: './app/metamask.html', to: "metamask.html" },
      { from: './app/error.html', to: "error.html" },
      { from: './app/404.html', to: "404.html" },
      { from: './app/assets', to: "assets" },
    ])
  ],
  module: {
    rules: [
    { 
      test: /\.css$/, 
      exclude: /(node_modules|bower_components)/, 
      use: [ 'style-loader', 'css-loader' ] 
    },
    { 
      test: /\.js$/, 
      exclude: /(node_modules|bower_components)/,
      use: [{
        loader: 'babel-loader',
        query: {
          presets: ['@babel/preset-env'],
          plugins: ['@babel/plugin-transform-runtime']
        }
      }]
    }]
  },
};