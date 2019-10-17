const gulp = require("gulp");
global.MODE = "development";

function setModeToDevelopment(cb) {
    global.MODE = "development";
    cb();
}

function setModeToProduction(cb) {
    global.MODE = "production";
    cb();
}


module.exports.default = gulp.series(
    require("./cms4py/SubProjects/FrontEnd/Register/gulpfile").default
);

module.exports.BuildRelease = gulp.series(
    setModeToProduction,
    module.exports.default
);

module.exports.BuildDebug = gulp.series(
    setModeToDevelopment,
    module.exports.default
);