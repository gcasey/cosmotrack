ct.views.SimulationView = Backbone.View.extend({
    initialize: function () {
        this.analyses = new ct.collections.AnalysisCollection();
        this.analyses.on('fetched', function () {
            this.render();
        }, this).fetch({
            simulation: this.model
        });
    },

    render: function () {
        this.$el.html(jade.templates.simulation({
            simulation: this.model
        }));
        new ct.views.AnalysisListView({
            el: this.$('.ct-analysis-wrapper'),
            analyses: this.analyses
        }).on('selected', function (analysis) {
            this.analysisSelected(analysis);
        }, this).render();

        new ct.views.MetadataView({
            el: this.$('.ct-params-wrapper'),
            model: this.model
        }).render();
        return this;
    },

    analysisSelected: function (analysis) {
        this.trigger('visualize', analysis);
        return this;
    }
});
