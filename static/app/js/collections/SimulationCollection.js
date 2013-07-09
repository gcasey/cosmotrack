ct.collections.SimulationCollection = Backbone.Collection.extend({
    model: ct.models.Simulation,

    fetch: function (opts) {
        ct.restRequest({
            resource: 'simulation'
        }).done(_.bind(function (resources) {
            this.add(resources);
            this.trigger('fetched');
        }, this));
    }
});
