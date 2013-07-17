ct.views.DashboardView = Backbone.View.extend({
    render: function () {
        this.$el.html(jade.templates.dashboard());

        this.resultListView = new ct.views.ResultListView({
            el: '#ct-result-list-well'
        });

        this.analysisView = new ct.views.AnalysisView({
            el: '#ct-analysis-well'
        }).render();

        this.resultListView.on('analysisSelected', function (analysis) {
            this.analysisView.setModel(analysis);
        }, this);

        return this;
    }
});
