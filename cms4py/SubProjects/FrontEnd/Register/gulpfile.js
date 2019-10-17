const gulp = require("gulp");
const path = require("path");
const webpack = require("webpack-stream");

const OUTPUT_FILE_NAME = "user_register.js";
const OUTPUT_DIR = path.join(__dirname, "..", '..', "..", 'static', "js");

function BuildProject() {
    return gulp.src(path.join(__dirname, "src", "main.js"))
        .pipe(webpack({
            mode: global.MODE || "development",
            module: {
                rules: [
                    {
                        test: /\.(html)$/,
                        use: {
                            loader: 'html-loader'
                        }
                    },
                    {
                        test: /\.css$/,
                        use: ['style-loader', 'css-loader']
                    }
                ]
            },
            output: {
                filename: OUTPUT_FILE_NAME
            }
        }))
        .pipe(gulp.dest(OUTPUT_DIR));
}

module.exports.default = gulp.series(BuildProject);