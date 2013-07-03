ct.views.ResultListView = Backbone.View.extend({
    initialize: function () {
        this.collection.on('add', function () {
            this.render();
        }, this);
    },

    render: function () {
        this.$el.empty().append(jade.templates.result_list({
            simulations: this.collection.models
        }));
        $('.ct-result-accordion').accordion({
            active: false,
            collapsible: true
        });
    }
});
