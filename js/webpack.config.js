//var fs = require("fs-extra");
var path = require("path");
var version = require("./package.json").version;

// Custom webpack rules are generally the same for all webpack bundles, hence
// stored in a separate local variable.
var rules = [{ test: /\.css$/, use: ["style-loader", "css-loader"] }];

// TODO: copy package.json so we can grab its version in glvis
module.exports = [
    { // Notebook extension
        entry: './src/extension.js',
        output: {
            filename: 'extension.js',
            path: path.resolve(__dirname, '..', 'glvis', 'nbextension'),
            libraryTarget: 'amd',
            publicPath: '',
        },
    },
    { // glvis-jupyter bundle for the classic notebook
        entry: './src/notebook.js',
        output: {
            filename: 'index.js',
            path: path.resolve(__dirname, '..', 'glvis', 'nbextension'),
            libraryTarget: 'amd',
            publicPath: '',
        },
        devtool: 'source-map',
        module: {
            rules: rules
        },
        externals: ['@jupyter-widgets/base'],
    },
    { // glvis-jupyter bundle for unpkg
        entry: './src/embed.js',
        output: {
            filename: 'index.js',
            path: path.resolve(__dirname, 'dist'),
            libraryTarget: 'amd',
            publicPath: 'https://unpkg.com/glvis-jupyter@' + version + '/dist/'
        },
        devtool: 'source-map',
        module: {
            rules: rules
        },
        externals: ['@jupyter-widgets/base'],
    }
];
