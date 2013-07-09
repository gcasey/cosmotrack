ct.views.SimulationView = Backbone.View.extend({
    initialize: function () {
        this.analyses = new ct.collections.AnalysisCollection();
        this.analyses.on('fetched', function () {
            this.render();
        }, this);
        this.analyses.fetch({
            simulation: this.model
        });
    },

    render: function () {
        this.$el.html(jade.templates.simulation({
            simulation: this.model,
            analyses: this.analyses.models
        }));
        return this;
    }
});
