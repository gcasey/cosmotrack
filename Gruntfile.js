module.exports = function (grunt) {
    var fs = require('fs');
    var path = require('path');

    // Project configuration.
    grunt.initConfig({
        pkg: grunt.file.readJSON('package.json'),

        jade: {
            inputDir: 'templates',
            outputFile: 'static/app/js/built/templates.js'
        },

        watch: {
            jade: {
                files: 'templates/*.jade',
                tasks: ['jade'],
                options: {failOnError: false}
            }
        }
    });
    grunt.loadNpmTasks('grunt-shell');
    grunt.loadNpmTasks('grunt-contrib-watch');
    grunt.loadNpmTasks('grunt-contrib-qunit');
    grunt.loadNpmTasks('grunt-contrib-stylus');

    // Compile the jade templates into a single js file
    grunt.registerTask('jade', 'Build the templates', function (inputFile) {
        var config = grunt.config.get ('jade');
        var outputFile = config.outputFile;
        var jade = require('jade');

        var task = this;
        var inputFiles = grunt.file.expand(config.inputDir+"/*.jade");

        fs.writeFileSync(outputFile, '\nvar jade=jade || {};jade.templates=jade.templates || {};\n');

        inputFiles.forEach(function (filename, i) {
            var buffer = fs.readFileSync(filename);
            var basename = path.basename(filename, '.jade');
            console.log('Compiling template: ' + basename);

            var fn = jade.compile(buffer, {
                client: true,
                compileDebug: false
            });

            var jt = "\njade.templates['" + basename + "'] = " + fn.toString() + ';';
            fs.appendFileSync(outputFile, jt);
        });
        console.log('Wrote ' + inputFiles.length + ' templates into ' + outputFile);
    });

    // Task to create symlink to node_modules in static if it doesn't exist already
    grunt.registerTask('symlink-packages', 'Add symlink for node modules', function () {
        if (!fs.existsSync('static/node')) {
            console.log('Symlink node_modules directory');
            fs.symlinkSync('../node_modules', 'static/node', 'dir');
        }
    });

    grunt.registerTask('default', ['jade', 'symlink-packages']);
};
