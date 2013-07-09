ct.collections.ViewableCollection = Backbone.Collection.extend({
    model: ct.models.Viewable,

    fetch: function (opts) {
        ct.restRequest({
            resource: 'analysis',
            data: {
                simulation_id: opts.simulation.id
            }
        }).done(_.bind(function (resources) {
            this.add(resources);
            this.trigger('fetched');
        }, this));
    }
});
