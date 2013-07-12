ct.views.DashboardView = Backbone.View.extend({
    render: function () {
        this.$el.html(jade.templates.dashboard());

        this.resultListView = new ct.views.ResultListView({
            el: '#ct-result-list-well'
        });

        this.visualizeView = new ct.views.VisualizeView({
            el: '#ct-visualize-well'
        }).render();

        this.resultListView.on('visualize', function (analysis) {
            this.visualizeView.visualize(analysis);
        }, this);

        return this;
    }
});
