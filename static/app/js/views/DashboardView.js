ct.views.DashboardView = Backbone.View.extend({
    render: function () {
        this.$el.empty().append(jade.templates.dashboard());
        new ct.views.ResultListView({
            el: '#ct-result-list-well',
            collection: new ct.collections.SimulationCollection()
        }).render();
    }
});
