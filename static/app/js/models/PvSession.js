ct.models.PvSession = Backbone.Model.extend({
    id: null,
    analysis_id: null,
    secret: null,
    url: null,

    /**
     * Request that the server create a new paraview web instance.
     * Triggers the 'created' event when complete.
     */
    create: function () {
        ct.restRequest({
            resource: 'pvsession',
            type: 'POST'
        }).done(_.bind(function (attributes) {
            this.set(attributes);
            this.trigger('created');
        }, this)).error(_.bind(function () {
            this.trigger('error');
        }, this));
    }
});
