ct.collections.SimulationCollection = Backbone.Collection.extend({
    model: ct.models.Simulation,

    initialize: function () {
        Backbone.ajax({
            url: ct.apiRoot + '/simulation',
            dataType: 'json'
        }).done(_.bind(function (resources) {
            this.add(resources);
        }, this));
    }
});
