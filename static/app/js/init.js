// This script must be invoked first to declare the ct namespace
var ct = {
    routes: {},
    models: {},
    collections: {},
    views: {},
    apiRoot: '/api/v1',

    restRequest: function (opts) {
        var defaults = {
            dataType: 'json',
            type: 'GET',

            /* To prevent this default behavior, pass in a opts object with an 'error'
               key. If you want a custom handler *in addition* to this behavior, add a
               ".error(...)" chained call on the returned object. */
            error: function (error) {
                ct.dialog({
                    title: 'API Error',
                    text: 'An error occurred while communicating with the server. ' +
                          'Details have been logged in the console.'
                });
                console.log(error.status + ' ' + error.statusText, error.responseText);
                ct.lastError = error;
            }
        };
        opts.url = ct.apiRoot + '/' + opts.resource;

        return Backbone.ajax($.extend(defaults, opts));
    }
};

// When all scripts are loaded, we invoke the application
$(function () {
    new ct.App({});
});
