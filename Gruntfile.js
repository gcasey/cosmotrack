module.exports = function (grunt) {
    var fs = require('fs');
    var path = require('path');

    // Project configuration.
    grunt.initConfig({
        pkg: grunt.file.readJSON('package.json'),

        jade: {
            inputDir: 'templates',
            outputFile: 'built/templates.js'
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

        fs.writeFileSync(outputFile, '\nif (jade.templates === undefined) jade.templates = {};\n;');

        inputFiles.forEach(function (filename, i) {
            var buffer = fs.readFileSync(filename);

            var fn = jade.compile(buffer, {
                client: true,
                compileDebug: false
            });

            var basename = path.basename(filename, '.jade');
            var jt = "\njade.templates['" + basename + "'] = " + fn.toString() + ';';
            fs.appendFileSync(outputFile, jt);
            console.log('Compiled template: ' + basename);
        });
        console.log('Wrote ' + inputFiles.length + ' templates into ' + outputFile);
    });

    grunt.registerTask('default', ['jade']);
};
