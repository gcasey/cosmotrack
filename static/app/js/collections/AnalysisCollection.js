ct.collections.AnalysisCollection = Backbone.Collection.extend({
    model: ct.models.Analysis,

    initialize: function (settings) {

        ct.restRequest({
            url: 'analysis'
        }).done(_.bind(function (resources) {
            console.log(resources);
            this.add(resources);
        }, this));
    }
});
