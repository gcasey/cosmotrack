ct.collections.SimulationCollection = Backbone.Collection.extend({
    model: ct.models.Simulation,

    initialize: function () {
        ct.restRequest({
            url: 'simulation'
        }).done(_.bind(function (resources) {
            console.log(resources);
            this.add(resources);
        }, this));
    }
});
