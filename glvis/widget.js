// Copyright (c) 2010-2024, Lawrence Livermore National Security, LLC. Produced
// at the Lawrence Livermore National Laboratory. All Rights reserved. See files
// LICENSE and NOTICE for details. LLNL-CODE-443271.
//
// This file is part of the GLVis visualization tool and library. For more
// information and source code availability see https://glvis.org.
//
// GLVis is free software; you can redistribute it and/or modify it under the
// terms of the BSD-3 license. We welcome feedback and contributions, see file
// CONTRIBUTING.md for details.

import glvis from "https://esm.sh/gh/glvis/glvis-js";

function render({ model, el }) {
  let div = document.createElement("div");
  div.setAttribute("id", glvis.rand_id());
  div.setAttribute("tabindex", "0");
  el.append(div);

  let width  = () => model.get("width");
  let height = () => model.get("height");
  let glv = new glvis.State(div, width(), height());

  function set_size() {
    glv.setSize(width(), height());
  }

  function plot() {
    const data = model.get("data_str");
    const is_new_stream = model.get("is_new_stream");
    if (is_new_stream) {
      glv.display(data);
    } else {
      glv.update(data);
    }
  }

  function handle_message(msg, buffers) {
    if (msg.type === "screenshot") {
      if (msg.use_web) {
        glv.saveScreenshot(msg.name);
      } else {
        glv.getPNGAsB64().then((v) => {
          model.send({ type: "screenshot", name: msg.name, b64: v });
        });
      }
    }
  }

  // update
  model.on("change:width", set_size);
  model.on("change:height", set_size);
  model.on("change:data_str", plot);
  model.on("msg:custom", handle_message);
  plot();
}

export default { render };
