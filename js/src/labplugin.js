var jupyter_glvis = require('./index');
var base = require('@jupyter-widgets/base');

module.exports = {
  id: 'jupyter-glvis',
  requires: [base.IJupyterWidgetRegistry],
  activate: function(app, widgets) {
      widgets.registerWidget({
          name: 'jupyter-glvis',
          version: jupyter_glvis.version,
          exports: jupyter_glvis
      });
  },
  autoStart: true
};

