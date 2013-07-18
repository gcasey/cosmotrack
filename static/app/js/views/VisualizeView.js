(function () {
    ct.views.VisualizeView = Backbone.View.extend({
        render: function () {
            this.$el.html(jade.templates.visualize());
            this.$status = this.$('span.ct-pvw-status-message');
            this.$overlay = this.$('.ct-pvw-overlay');
            this.$loading = this.$('img.ct-pvw-loading');

            this.colorByView = new ct.views.ColorByView({
                el: this.$('.ct-color-by-container')
            }).on('arrayNameSelected', function (arrayName) {
                this.colorBy(arrayName);
            }, this).render();

            return this;
        },

        visualize: function (analysis) {
            this.analysis = analysis;

            if (this.pvConnection) {
                // Reuse the already connected session
                loadAnalysis(this);
            }
            else {
                // Create a new session and connect to it
                this.pvSession = new ct.models.PvSession({
                    analysis_id: analysis.id
                });
                this.showStatus('Creating new ParaView session...', true);
                this.pvSession.on('created', function () {
                    this.showStatus('Connecting to session...', true);
                    connectToSession(this);
                }, this).on('error', function () {
                    this.showStatus('Create session failed.');
                }, this).create();
            }
            return this;
        },

        showStatus: function (message, loading) {
            this.$overlay.show();
            this.$status.text(message);
            if (loading) {
                this.$loading.show();
            }
            else {
                this.$loading.hide();
            }
        },

        hideStatus: function () {
            this.$overlay.hide();
        },

        colorBy: function (params) {
            var that = this;
            this.showStatus('Changing color function...', true);
            this.pvConnection.session.call('pv:colorBy', params.name, params.min, params.max)
              .then(function () {
                that.viewport.render();
                that.hideStatus();
            }).otherwise(function (err) {
                that.showStatus('An error occurred.');
                console.log(err);
            });
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
            sessionManagerURL: ct.apiRoot + '/pvsession',
            secret: view.pvSession.get('secret'),
            interactiveQuality: 60
        };

        paraview.connect(view.pvConfig, function(conn) {
            view.pvConnection = conn;
            view.viewport = paraview.createViewport(conn);
            view.viewport.bind('#ct-render-container');

            bindStop(view.pvConfig);
            loadAnalysis(view);
        }, function(code, msg) {
            view.pvConnection = null;
            view.pvSession = null;
            view.viewport.unbind();
            view.showStatus('Connection closed.');
            view.trigger('pvclosed', code, msg);
        });
    };

    /**
     * Private helper function to load an analysis in an existing pvSession
     * @param {VisualizeView} view The view object
     */
    var loadAnalysis = function (view) {
        var args = view.analysis.get('loadDataArgs');

        view.showStatus('Loading analysis data...', true);

        view.pvConnection.session.call('pv:loadData', args)
            .then(function (retVal) {
                view.colorByView.arrayList = retVal.infoArrays;
                view.colorByView.render();
                view.viewport.render();
                view.hideStatus();
            }).otherwise(function (err) {
                view.showStatus('Failed to load data');
                console.log(err);
            });
    };

    /**
     * Binds stopping the connection to the window unloading.
     * @param conf The ParaViewWeb configuration object
     */
    var bindStop = function (conf) {
        $(window).bind('beforeunload', function () {
            // We have to call this synchronously for it to work here.
            $.ajax({
                url: ct.apiRoot + '/pvsession/' + conf.id,
                async: false,
                type: 'DELETE'
            });
        });
    };
}) ();
