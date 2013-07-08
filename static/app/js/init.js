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
            type: 'GET'
        };
        opts.url = ct.apiRoot + opts.url;

        return Backbone.ajax($.extend(defaults, opts));
    }
};

// When all scripts are loaded, we invoke the application
$(function () {
    new ct.App({});
});
