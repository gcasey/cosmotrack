/**
 * Displays a clickable list of analyses
 */
ct.views.AnalysisListView = Backbone.View.extend({
    events: {
        'click .ct-analysis-link': 'analysisSelected'
    },

    initialize: function (settings) {
        this.analyses = settings.analyses;
    },

    render: function () {
        this.$el.html(jade.templates.analyses({
            analyses: this.analyses.models
        }));
        return this;
    },

    analysisSelected: function (event) {
        var link = $(event.currentTarget);
        var analysisId = link.attr('analysis-id');
        $('li.ct-analysis-result').removeClass('active');
        link.parent().addClass('active');

        this.trigger('selected', this.analyses.get(analysisId));
        return this;
    }
});
