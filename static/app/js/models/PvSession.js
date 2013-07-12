ct.models.PvSession = Backbone.Model.extend({
    id: null,
    analysis_id: null,
    secret: null,
    url: null,
    authKey: null,

    /**
     * Request that the server create a new paraview web instance.
     * Triggers the 'created' event when complete.
     */
    create: function () {
        ct.restRequest({
            resource: 'pvsession',
            type: 'POST',
            data: {
                analysis_id: this.get('analysis_id')
            }
        }).done(_.bind(function (attributes) {
            this.set(attributes);
            this.trigger('created');
        }, this)).error(_.bind(function () {
            this.trigger('error');
        }, this));
    }
});
