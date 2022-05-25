// Copyright (c) 2010-2021, Lawrence Livermore National Security, LLC. Produced
// at the Lawrence Livermore National Laboratory. All Rights reserved. See files
// LICENSE and NOTICE for details. LLNL-CODE-443271.
//
// This file is part of the GLVis visualization tool and library. For more
// information and source code availability see https://glvis.org.
//
// GLVis is free software; you can redistribute it and/or modify it under the
// terms of the BSD-3 license. We welcome feedback and contributions, see file
// CONTRIBUTING.md for details.

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
    this.width = this.model.get("width");
    this.height = this.model.get("height");

    this.glv = new glvis.State(this.div, this.width, this.height);
    this.model.on("change:data_str", this.plot, this);
    this.model.on("change:height", this.set_size, this);
    this.model.on("change:width", this.set_size, this);
    this.model.on("msg:custom", this.handle_message, this);
    this.plot();
  },

  handle_message: function (msg, buffers) {
    if (msg.type === "screenshot") {
      if (msg.use_web) {
        this.glv.saveScreenshot(msg.name);
      } else {
        let that = this;
        this.glv.getPNGAsB64().then((v) => {
          that.send({ type: "screenshot", name: msg.name, b64: v });
        });
      }
    }
  },

  set_size: function () {
    const width = this.model.get("width");
    const height = this.model.get("height");
    this.glv.setSize(width, height);
  },

  plot: function () {
    const type = this.model.get("data_type");
    const data = this.model.get("data_str");

    const is_new_stream = this.model.get("is_new_stream");
    if (is_new_stream) {
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
