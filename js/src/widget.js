var widgets = require("@jupyter-widgets/base");
var glvis = require("glvis");
var lodash = require("lodash");

// https://stackoverflow.com/questions/6860853/generate-random-string-for-div-id/6860916
// prettier-ignore
function guid() {
  var S4 = function() {
     return (((1+Math.random())*0x10000)|0).toString(16).substring(1);
  };
  return (S4()+S4()+"-"+S4()+"-"+S4()+"-"+S4()+"-"+S4()+S4()+S4());
}

var version = require("../package.json").version;

var GlvisModel = widgets.DOMWidgetModel.extend({
  defaults: lodash.extend(widgets.DOMWidgetModel.prototype.defaults(), {
    _model_name: "GlvisModel",
    _model_module: "glvis-jupyter",
    _model_module_version: "^" + version,

    _view_name: "GlvisView",
    _view_module: "glvis-jupyter",
    _view_module_version: "^" + version,
  }),
});

var GlvisView = widgets.DOMWidgetView.extend({
  render: function () {
    this.div = document.createElement("div");
    this.div.setAttribute("id", guid());
    this.div.setAttribute("tabindex", "0");
    this.el.append(this.div);

    this.canvas = glvis.setupCanvas(
      this.div,
      this.model.get("_width"),
      this.model.get("_height")
    );

    this.model.on("change:_data_str", this.display, this);
    this.display();
  },

  display: function () {
    // TODO: support dynamic size? that.model.get('_width'), that.model.get('_height')
    glvis.display(
      this.div,
      this.canvas,
      this.model.get("_data_type"),
      this.model.get("_data_str")
    );
  },
});

module.exports = {
  GlvisModel: GlvisModel,
  GlvisView: GlvisView,
};
