var widgets = require('@jupyter-widgets/base');
var glvis = require('./libglvis');
var lodash = require('lodash');

// https://stackoverflow.com/questions/6860853/generate-random-string-for-div-id/6860916
function guid() {
    var S4 = function() {
       return (((1+Math.random())*0x10000)|0).toString(16).substring(1);
    };
    return (S4()+S4()+"-"+S4()+"-"+S4()+"-"+S4()+"-"+S4()+S4()+S4());
}

var version = require("../package.json").version;

var GlvisModel = widgets.DOMWidgetModel.extend({
    defaults: lodash.extend(widgets.DOMWidgetModel.prototype.defaults(), {
        _model_name : 'GlvisModel',
        _model_module : 'jupyter-glvis',
        _model_module_version : '^' + version,

        _view_name : 'GlvisView',
        _view_module : 'jupyter-glvis',
        _view_module_version : '^' + version
    })
});

var GlvisView = widgets.DOMWidgetView.extend({
    render: function() {
        var that = this;
        this.div_wrapper = document.createElement('div');
        this.div_id = guid();
        this.div_wrapper.setAttribute('id', this.div_id);
        this.div_wrapper.setAttribute('tabindex', '0');

        this.canvas = document.createElement('canvas');
        this.canvas.setAttribute('oncontextmenu', 'return false;');
        // clicks focus on the div which is the keyboard target for SDL,
        // set with {glvis_instance}.setKeyboardListeningElementId
        this.canvas.addEventListener('click', function() {
            that.div_wrapper.focus();
            return true;
        });

        this.div_wrapper.append(this.canvas);
        this.el.append(this.div_wrapper);
        this.model.on('change:_data_str', this.display, this);
        this.display();
    },

    display: function() {
        var that = this;
        glvis().then(function(g) {
            g.setKeyboardListeningElementId(that.div_id);
            g.canvas = that.canvas;
            g.startVisualization(that.model.get('_data_str'), that.model.get('_data_type'),
              that.model.get('_width'), that.model.get('_height'));
            function iter(timestamp) {
                g.iterVisualization();
                window.requestAnimationFrame(iter);
            }
            window.requestAnimationFrame(iter);
        }, function(err) {
          console.log(err);
        });
    }
});

module.exports = {
    GlvisModel : GlvisModel,
    GlvisView : GlvisView
};
