module.exports = function(grunt) {
  grunt.initConfig({
    markdownpdf: {
      options: {},
      files: {
        src: "*.md",
        dest: "./"
      }
    }
  });

  grunt.loadNpmTasks('grunt-markdown-pdf');

  grunt.registerTask('default', ['markdownpdf']);
};
