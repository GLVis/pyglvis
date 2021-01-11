// Copyright (c) 2010-2020, Lawrence Livermore National Security, LLC. Produced
// at the Lawrence Livermore National Laboratory. All Rights reserved. See files
// LICENSE and NOTICE for details. LLNL-CODE-443271.
//
// This file is part of the GLVis visualization tool and library. For more
// information and source code availability see https://glvis.org.
//
// GLVis is free software; you can redistribute it and/or modify it under the
// terms of the BSD-3 license. We welcome feedback and contributions, see file
// CONTRIBUTING.md for details.

// This file contains the javascript that is run when the notebook is loaded.
// It contains some requirejs configuration and the `load_ipython_extension`
// which is required for any notebook extension.

// Some static assets may be required by the custom widget javascript. The base
// url for the notebook is not known at build time and is therefore computed
// dynamically.
__webpack_public_path__ =
  document.querySelector("body").getAttribute("data-base-url") +
  "nbextensions/glvis-jupyter";

// Configure requirejs
if (window.require) {
  window.require.config({
    map: {
      "*": {
        "glvis-jupyter": "nbextensions/glvis-jupyter/index",
      },
    },
  });
}

// Export the required load_ipython_extension
module.exports = {
  load_ipython_extension: function () {},
};
