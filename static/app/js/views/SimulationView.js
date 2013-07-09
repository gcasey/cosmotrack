ct.views.SimulationView = Backbone.View.extend({
    initialize: function () {
        this.viewables = new ct.collections.ViewableCollection();
        this.viewables.on('fetched', function () {
            this.render();
        }, this);
        this.viewables.fetch({
            simulation: this.model
        });
    },

    render: function () {
        this.$el.html(jade.templates.simulation({
            simulation: this.model,
            viewables: this.viewables.models
        }));
        return this;
    }
});
