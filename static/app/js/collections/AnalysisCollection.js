ct.collections.AnalysisCollection = Backbone.Collection.extend({
    model: ct.models.Analysis,

    initialize: function (settings) {

        Backbone.ajax({
            url: ct.apiRoot + '/analysis',
            dataType: 'json'
        }).done(_.bind(function (resources) {
            console.log(resources);
            this.add(resources);
        }, this));
    }
});
