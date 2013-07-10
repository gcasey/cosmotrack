(function () {
    ct.views.VisualizeView = Backbone.View.extend({
        render: function () {
            this.$el.html(jade.templates.visualize());
            this.$status = this.$('span.ct-pvw-status-message');
            this.$overlay = this.$('.ct-pvw-overlay');
            return this;
        },

        visualize: function (analysisId) {
            if (this.pvSession) {
                // TODO use existing session
            }
            else {
                this.pvSession = new ct.models.PvSession({
                    analysis_id: analysisId
                });
                this.$overlay.show();
                this.$status.text('Creating new ParaView session...');
                this.pvSession.on('created', function() {
                    this.$status.text('Connecting to session...');
                    connectToSession(this, this.pvSession);
                }, this).create();
            }
            return this;
        }
    });

    var connectToSession = function (view, pvSession) {
        console.log(view);
        console.log(pvSession);
    };
}) ();
