ct.views.AnalysisView = Backbone.View.extend({
    initialize: function () {
        // Initialize with an empty model until an analysis is selected
        // and this.setModel is called.
        this.model = new ct.models.Analysis({
            id: null,
            params: []
        });
    },

    render: function () {
        this.$el.html(jade.templates.analysis({
            analysis: this.model
        }));

        this.visualizeView = new ct.views.VisualizeView({
            el: this.$('.ct-visualize-wrapper')
        }).render();

        this.metadataView = new ct.views.MetadataView({
            el: this.$('.ct-analysis-metadata-wrapper'),
            model: this.model
        }).render();

        return this;
    },

    setModel: function (analysis) {
        this.model = analysis;
        this.visualizeView.visualize(analysis);
        this.metadataView.model = analysis;
        console.log(this.metadataView.model);
        this.metadataView.render();
    }
});
