ct.App = Backbone.View.extend({
    el: 'body',

    initialize: function (settings) {
        this.render();

        new ct.views.DashboardView({
            el: '#ct-main-content'
        }).render();

        Backbone.history.start({
            pushState: false,
            root: settings.root
        });
    },

    render: function () {
        this.$el.html(jade.templates.app());
    }
});
