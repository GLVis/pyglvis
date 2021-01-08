var widgets = require("@jupyter-widgets/base");
var glvis = require("glvis");
var lodash = require("lodash");
var version = require("../package.json").version;

var GLVisModel = widgets.DOMWidgetModel.extend({
  defaults: lodash.extend(widgets.DOMWidgetModel.prototype.defaults(), {
    _model_name: "GLVisModel",
    _model_module: "glvis-jupyter",
    _model_module_version: "^" + version,

    _view_name: "GLVisView",
    _view_module: "glvis-jupyter",
    _view_module_version: "^" + version,
  }),
});

var GLVisView = widgets.DOMWidgetView.extend({
  render: function () {
    this.div = document.createElement("div");
    this.div.setAttribute("id", glvis.rand_id());
    this.div.setAttribute("tabindex", "0");
    this.el.append(this.div);
    this.width = this.model.get("_width");
    this.height = this.model.get("_height");

    this.glv = new glvis.State(this.div, this.width, this.height);
    this.model.on("change:_data_str", this.visualize, this);
    this.model.on("change:_height", this.resize, this);
    this.model.on("change:_width", this.resize, this);
    this.visualize();
  },

  resize: function () {
    const width = this.model.get("_width");
    const height = this.model.get("_height");
    this.glv.setSize(width, height);
  },

  visualize: function () {
    const type = this.model.get("_data_type");
    const data = this.model.get("_data_str");

    const new_stream = this.model.get("_new_stream");
    if (new_stream) {
      this.glv.display(type, data);
    } else {
      this.glv.update(type, data);
    }
  },
});

module.exports = {
  GLVisModel: GLVisModel,
  GLVisView: GLVisView,
  version: version,
};
