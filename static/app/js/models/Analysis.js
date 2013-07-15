ct.models.Analysis = Backbone.Model.extend({
    id: null,
    name: null,
    loadDataArgs: null,

    validate : function(attrs, options) {
        if (attrs.loadDataArgs === null) {
            return 'Load data not specified';
        }
    }
});
