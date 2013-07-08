ct.views.ResultListView = Backbone.View.extend({
    events: {
        'click .ct-accordion-header': 'displaySimulation'
    },

    initialize: function () {
        this.collection.on('fetched', function () {
            this.render();
        }, this);
    },

    render: function () {
        this.$el.empty().append(jade.templates.result_list({
            simulations: this.collection.models
        }));
        this.accordion = $('.ct-result-accordion').accordion({
            active: false,
            collapsible: true,
            heightStyle: 'content'
        });
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
    }
});
