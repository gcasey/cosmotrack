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

    /**
     * Private helper function to connect to PVW session that has started
     */
    var connectToSession = function (view, pvSession) {
        view.pvConfig = {
            sessionURL: pvSession.get('url'),
            id: pvSession.id,
            sessionManagerURL: ct.apiRoot + 'pvsession',
            //secret: pvSession.get('authKey'),
            interactiveQuality: 50
        };
        paraview.connect(view.pvConfig, function(conn) {
            view.pvConnection = conn;
            view.viewport = paraview.createViewport(conn);
            view.viewport.bind('#ct-render-container');

            view.$overlay.hide();
        }, function(code, msg) {
            view.$status.text('Connection failed.');
            view.$('img.ct-pvw-loading').hide();
            view.trigger('pverror', code, msg);
        });
    };
}) ();
