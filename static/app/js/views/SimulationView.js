ct.views.SimulationView = Backbone.View.extend({
    initialize: function () {
        this.viewables = new ct.collections.ViewableCollection({
            simulation: this.model
        });
        this.viewables.on('fetched', function () {
            this.render();
        }, this);
    },

    render: function () {
        this.$el.empty().append(jade.templates.simulation({
            simulation: this.model,
            viewables: this.viewables.models
        }));
    }
});
