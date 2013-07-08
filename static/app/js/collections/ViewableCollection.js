ct.collections.ViewableCollection = Backbone.Collection.extend({
    model: ct.models.Viewable,

    initialize: function (settings) {
        ct.restRequest({
            resource: 'viewable',
            data: {
                simulation_id: settings.simulation.id
            }
        }).done(_.bind(function (resources) {
            this.add(resources);
            this.trigger('fetched');
        }, this));
    }
});
