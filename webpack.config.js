module.exports = {
    entry: {
        main: "./api/static/js/index.js",
    },
    module: {
        rules: [
            {
                test: /\.js$/,
                use: "babel-loader",
            },
            {
                test: /\.(svg|png|jpg|jpeg|gif)$/,
                loader: "file-loader",
                options: {
                    name: "[name].[ext]",
                    outputPath: "../../api/static/dist",
                },
            },
            {
                test: /\.css$/i,
                use: ["style-loader", "css-loader"],
            },
            {
                test: /\.(scss)$/,
                use: [
                    {
                        loader: 'style-loader', // inject CSS to page
                    }, {
                        loader: 'css-loader', // translates CSS into CommonJS modules
                    }, {
                        loader: 'postcss-loader', // Run post css actions
                        options: {
                          plugins: function () { 
                            // post css plugins, can be exported to postcss.config.js
                            return [
                              require('precss'),
                              require('autoprefixer')
                            ];
                          }
                        }
                    }, {
                        loader: 'sass-loader',
                        options: {
                            sassOptions: {
                                indentedSyntax: false
                            }
                        }
                    }
                ]
            }
        ]
    },
    output: {
        path: __dirname + "/api/static/dist",
        filename: "[name].bundle.js",
    },
};
