ct.views.ColorByView = Backbone.View.extend({
    events: {
        'click .ct-color-by-list li a': 'arrayNameSelected'
    },

    initialize: function (settings) {
        this.arrayList = settings.arrayList || [];
    },

    render: function () {
        this.$el.html(jade.templates.color_by({
            arrayList: this.arrayList
        }));
        if (this.arrayList.length > 0) {
            this.$('.ct-color-by-button').removeClass('disabled');
        }
        return this;
    },

    arrayNameSelected: function (event) {
        var link = $(event.currentTarget);
        this.trigger('arrayNameSelected', {
            name: link.attr('name'),
            min: parseFloat(link.attr('min')),
            max: parseFloat(link.attr('max')),
            type: link.attr('type')
        });
    }
});
