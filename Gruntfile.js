module.exports = function (grunt) {
    var fs = require('fs');
    var path = require('path');

    // Project configuration.
    grunt.initConfig({
        pkg: grunt.file.readJSON('package.json'),

        config: {
            // The order of this list represents the order of script imports and execution
            srcList: [
                // Third-party libraries
                'lib/js/jquery-1.10.1.min.js',
                'lib/js/jquery-ui.min.js',
                'lib/js/bootstrap.min.js',
                'node/jade/runtime.js',
                'node/underscore/underscore-min.js',
                'node/backbone/backbone-min.js',

                // Application imports
                'app/js/built/templates.js',
                'app/js/init.js',

                'app/js/models/Analysis.js',
                'app/js/models/Simulation.js',
                'app/js/collections/AnalysisCollection.js',
                'app/js/collections/SimulationCollection.js',
                'app/js/views/ResultListView.js',
                'app/js/views/DashboardView.js',
                'app/js/views/SimulationView.js',

                'app/js/router.js',
                'app/js/app.js'
            ]
        },

        jade: {
            inputDir: 'templates',
            outputFile: 'static/app/js/built/templates.js'
        },

        stylus: {
            compile: {
                files: {'static/app/css/built/cosmotrack.css': ['stylesheets/*.styl']}
            }
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

    // Put all of our js into one file
    grunt.registerTask('build-js', 'Compile the JS into a single file', function () {
        var config = grunt.config.get('config');
        var compiledFile = 'static/app/js/built/cosmotrack.js';
        if (fs.existsSync(compiledFile)) {
            fs.unlinkSync(compiledFile);
        }

        config.srcList.forEach(function (srcFile) {
            console.log('Appending ' + srcFile)
            var content = fs.readFileSync('static/' + srcFile);
            fs.appendFileSync(compiledFile, content + '\n;\n');
        });
    });

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

    grunt.registerTask('default', ['jade', 'build-js', 'stylus', 'symlink-packages']);
};
