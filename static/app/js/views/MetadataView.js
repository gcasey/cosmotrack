/**
 * This view displays the list of params for either
 * a simulation or an analysis. As such, it should
 * only contain elements corresponding to both types.
 *
 * Should be constructed with a model parameter.
 */
ct.views.MetadataView = Backbone.View.extend({
    render: function () {
        this.$el.html(jade.templates.metadata({
            params: this.model.get('params')
        }));
        return this;
    }
});
