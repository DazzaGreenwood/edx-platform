define(["jquery", "underscore", "js/views/baseview"],
    function ($, _, BaseView) {

        var NewComponentMenu = BaseView.extend({
            initialize : function() {
                BaseView.prototype.initialize.call(this);
                this.template = this.loadTemplate("add-xblock-component-menu");
                this.$el.html(this.template({type: this.model.type, templates: this.model.templates}));
            }
        });

        return NewComponentMenu;
    }); // end define();