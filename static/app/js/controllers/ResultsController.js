ct.controllers.ResultsController = Backbone.View.extend({
    render: function () {
        this.$el.append(jade.templates.results());
    }
});
