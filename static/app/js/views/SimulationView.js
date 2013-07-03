ct.views.SimulationView = Backbone.View.extend({
    render: function () {
        this.$el.empty().append(jade.templates.simulation({
            simulation: this.model
        }));
    }
});
