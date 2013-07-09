// This script must be invoked first to declare the ct namespace
var ct = {
    routes: {},
    models: {},
    collections: {},
    views: {},
    apiRoot: '/api/v1/',

    restRequest: function (opts) {
        var defaults = {
            dataType: 'json',
            type: 'GET',
            error: function (error) {
                ct.dialog({
                    title: 'API Error',
                    text: 'An error occurred while communicating with the server. ' +
                          'Details have been logged in the console.'
                });
                console.log(error);
            }
        };
        opts.url = ct.apiRoot + opts.resource;

        return Backbone.ajax($.extend(defaults, opts));
    }
};

// When all scripts are loaded, we invoke the application
$(function () {
    new ct.App({});
});
