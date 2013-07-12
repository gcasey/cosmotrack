(function () {
    ct.views.VisualizeView = Backbone.View.extend({
        render: function () {
            this.$el.html(jade.templates.visualize());
            this.$status = this.$('span.ct-pvw-status-message');
            this.$overlay = this.$('.ct-pvw-overlay');
            this.$loading = this.$('img.ct-pvw-loading');
            return this;
        },

        visualize: function (analysis) {
            this.analysis = analysis;

            if (this.pvConnection) {
                // Reuse the already connected session
                this.$overlay.show();
                this.$loading.show();
                this.$status.text('Loading analysis data...');
                loadAnalysis(this);
            }
            else {
                // Create a new session and connect to it
                this.pvSession = new ct.models.PvSession({
                    analysis_id: analysis.id
                });
                this.$overlay.show();
                this.$status.text('Creating new ParaView session...');
                this.pvSession.on('created', function () {
                    this.$status.text('Connecting to session...');
                    connectToSession(this);
                }, this).on('error', function () {
                    this.$loading.hide();
                    this.$status.text('Create session failed.');
                }, this).create();
            }
            return this;
        }
    });

    /**
     * Private helper function to connect to PVW session that has started
     * @param {VisualizeView} view The view object
     */
    var connectToSession = function (view) {
        view.pvConfig = {
            sessionURL: view.pvSession.get('url'),
            id: view.pvSession.id,
            sessionManagerURL: ct.apiRoot + 'pvsession',
            //secret: view.pvSession.get('authKey'),
            interactiveQuality: 50
        };
        paraview.connect(view.pvConfig, function(conn) {
            view.pvConnection = conn;
            view.viewport = paraview.createViewport(conn);
            view.viewport.bind('#ct-render-container');
            loadAnalysis(view);

            view.$overlay.hide();
        }, function(code, msg) {
            view.$status.text('Connection failed.');
            view.$loading.hide();
            view.trigger('pverror', code, msg);
        });
    };

    /**
     * Private helper function to load an analysis in an existing pvSession
     * @param {VisualizeView} view The view object
     */
    var loadAnalysis = function (view) {
        var args = view.analysis.loadDataArgs;
        view.pvConnection.session.call('pv:loadData', args, function () {
            view.viewport.render();
        });
    };
}) ();
