ct.views.SimulationView = Backbone.View.extend({
    events: {
        'click .ct-analysis-link': 'requestVisualization'
    },

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
    },

    requestVisualization: function (event) {
        var link = $(event.currentTarget);
        var analysisId = link.attr('analysis-id');
        $('li.ct-analysis-result').removeClass('active');
        link.parent().addClass('active');

        this.trigger('visualize', this.analyses.get(analysisId));
    }
});
