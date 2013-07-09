ct.views.SimulationView = Backbone.View.extend({
    initialize: function () {
        this.analysiscollection = new ct.collections.ViewableCollection();
        this.analysiscollection.on('fetched', function () {
            this.render();
        }, this);
        this.analysiscollection.fetch({
            simulation: this.model
        });
    },

    render: function () {
        this.$el.html(jade.templates.simulation({
            simulation: this.model,
            analysiscollection: this.analysiscollection.models
        }));
        return this;
    }
});
