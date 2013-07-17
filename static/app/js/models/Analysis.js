ct.models.Analysis = Backbone.Model.extend({
    id: null,
    name: null,
    loadDataArgs: null,
    params: [],

    validate: function(attrs) {
        if (attrs.loadDataArgs === null) {
            return 'Load data not specified';
        }
    }
});
