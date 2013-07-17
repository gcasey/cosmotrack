module.exports = function (grunt) {
    var fs = require('fs');
    var path = require('path');

    // Project configuration.
    grunt.initConfig({
        pkg: grunt.file.readJSON('package.json'),

        config: {
            // The order of these lists represents the order of script imports and execution
            libSrcList: [
                // Third-party libraries
                'lib/js/jquery-1.10.1.min.js',
                'lib/js/jquery-ui.min.js',
                'lib/js/bootstrap.min.js',
                'lib/js/underscore-min.js',
                'lib/js/autobahn.min.js',
                'lib/js/paraview-all.min.js',
                'lib/js/hammer.min.js',
                'lib/js/jquery.hammer.min.js',
                'node/jade/runtime.js',
                'node/backbone/backbone-min.js'
            ],
            appSrcList: [
                // Application files
                'app/js/built/templates.js',
                'app/js/init.js',

                'app/js/models/Analysis.js',
                'app/js/models/PvSession.js',
                'app/js/models/Simulation.js',
                'app/js/collections/AnalysisCollection.js',
                'app/js/collections/SimulationCollection.js',
                'app/js/views/AnalysisView.js',
                'app/js/views/AnalysisListView.js',
                'app/js/views/MetadataView.js',
                'app/js/views/ResultListView.js',
                'app/js/views/DashboardView.js',
                'app/js/views/SimulationView.js',
                'app/js/views/VisualizeView.js',

                'app/js/utilities.js',
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
                files: {
                    'static/app/css/built/cosmotrack.css': ['stylesheets/*.styl']
                }
            }
        },

        uglify: {
            cosmotrack: {
                files: {
                    'static/app/js/built/cosmotrack.min.js': ['static/app/js/built/cosmotrack.js']
                }
            }
        },

        watch: {
            css: {
                files: 'stylesheets/*.styl',
                tasks: ['build-css'],
                options: {failOnError: false}
            },
            js: {
                files: ['static/app/js/**/*.js',
                        '!static/app/js/built/*.js'],
                tasks: ['concat-js', 'uglify'],
                options: {failOnError: false}
            },
            jade: {
                files: ['templates/*.jade'],
                tasks: ['build-js'],
                options: {failOnError: false}
            }
        }
    });
    grunt.loadNpmTasks('grunt-shell');
    grunt.loadNpmTasks('grunt-contrib-watch');
    grunt.loadNpmTasks('grunt-contrib-qunit');
    grunt.loadNpmTasks('grunt-contrib-stylus');
    grunt.loadNpmTasks('grunt-contrib-uglify');

    // Put all of our js into one file
    grunt.registerTask('concat-js', 'Compile the JS into a single file', function () {
        var config = grunt.config.get('config');
        var compiledLibs = 'static/app/js/built/libs.js',
            compiledApp  = 'static/app/js/built/cosmotrack.js';

        if (fs.existsSync(compiledLibs)) {
            fs.unlinkSync(compiledLibs);
        }
        if (fs.existsSync(compiledApp)) {
            fs.unlinkSync(compiledApp);
        }

        console.log('Building libs.js');
        config.libSrcList.forEach(function (srcFile) {
            console.log('Appending ' + srcFile)
            var content = fs.readFileSync('static/' + srcFile);
            fs.appendFileSync(compiledLibs, content + '\n;\n');
        });

        console.log('Building cosmotrack.js');
        config.appSrcList.forEach(function (srcFile) {
            console.log('Appending ' + srcFile)
            var content = fs.readFileSync('static/' + srcFile);
            fs.appendFileSync(compiledApp, content + '\n\n');
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

    grunt.registerTask('init', 'One-time tasks', function () {
        if (!fs.existsSync('static/node')) {
            console.log('Symlinking node_modules directory');
            fs.symlinkSync('../node_modules', 'static/node', 'dir');
        }
        if (!fs.existsSync('server/paraview.local.cfg')) {
            console.log('Creating local config file');
            fs.writeFileSync('server/paraview.local.cfg', fs.readFileSync('server/paraview.cfg'));
        }
    });

    grunt.registerTask('build-css', ['stylus'])
    grunt.registerTask('build-js', ['jade', 'concat-js', 'uglify']);
    grunt.registerTask('default', ['init', 'build-css', 'build-js']);
};
