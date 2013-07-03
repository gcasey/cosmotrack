var ct = {
    routes: {},
    models: {},
    collections: {},
    views: {},
    apiRoot: '/api/v1'
};

// When all scripts are loaded, we invoke the application
$(function () {
    new ct.App({});
});
