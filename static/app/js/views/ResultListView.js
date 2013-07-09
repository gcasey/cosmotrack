ct.views.ResultListView = Backbone.View.extend({
    events: {
        'click .ct-accordion-header': 'displaySimulation',
        'click a.ct-analysis-link': 'requestVisualization'
    },

    initialize: function () {
        this.collection = new ct.collections.SimulationCollection();
        this.collection.on('fetched', function () {
            this.render();
        }, this);
        this.collection.fetch();
    },

    render: function () {
        this.$el.html(jade.templates.result_list({
            simulations: this.collection.models
        }));
        this.accordion = $('.ct-result-accordion').accordion({
            active: false,
            collapsible: true,
            heightStyle: 'content'
        });
        return this;
    },

    displaySimulation: function (event) {
        var $header = $(event.target);
        var simulationId = $header.attr('simulation-id');
        var container = $header.next();

        if (!container.hasClass('ct-fetched')) {
            container.addClass('ct-fetched');

            new ct.views.SimulationView({
                el: container,
                model: this.collection.get(simulationId),
            });
        }
    },

    requestVisualization: function (event) {
        var analysisId = $(event.target).attr('analysis-id');
        this.trigger('visualize', analysisId);
    }
});
