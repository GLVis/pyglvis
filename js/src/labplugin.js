var glvis_jupyter = require("./index");
var base = require("@jupyter-widgets/base");

module.exports = {
  id: "glvis-jupyter",
  requires: [base.IJupyterWidgetRegistry],
  activate: function (app, widgets) {
    widgets.registerWidget({
      name: "glvis-jupyter",
      version: glvis_jupyter.version,
      exports: glvis_jupyter,
    });
  },
  autoStart: true,
};
