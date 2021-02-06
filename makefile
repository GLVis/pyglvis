# Copyright (c) 2010-2021, Lawrence Livermore National Security, LLC. Produced
# at the Lawrence Livermore National Laboratory. All Rights reserved. See files
# LICENSE and NOTICE for details. LLNL-CODE-443271.
#
# This file is part of the GLVis visualization tool and library. For more
# information and source code availability see https://glvis.org.
#
# GLVis is free software; you can redistribute it and/or modify it under the
# terms of the BSD-3 license. We welcome feedback and contributions, see file
# CONTRIBUTING.md for details.

NPX   ?= npx
BLACK ?= black

.PHONY: style

style:
	@which $(NPX) > /dev/null && (cd js && $(NPX) prettier -w .) || echo "fatal: $(NPX) isn't available, please install npm to format JavaScript."
	@which $(BLACK) > /dev/null && $(BLACK) . || echo "fatal: $(BLACK) isn't available, please install black to format Python."

clean:
	rm -rf js/node_modules js/dist glvis/nbextension glvis.egg-info
