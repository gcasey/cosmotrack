var ct = {
    routes: {},
    models: {},
    collections: {},
    views: {},
    controllers: {}
};

// When all scripts are loaded, we invoke the application
$(function () {
    new ct.App({});
});
