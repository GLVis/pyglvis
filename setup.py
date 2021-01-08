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

from __future__ import print_function
from distutils import log
import os
import platform
from setuptools import setup, find_packages, Command
from setuptools.command.sdist import sdist
from setuptools.command.build_py import build_py
from setuptools.command.egg_info import egg_info
from subprocess import check_call
import sys

name = "glvis"
long_description = "Jupyter Widget for GLVis"

here = os.path.dirname(os.path.abspath(__file__))
node_root = os.path.join(here, "js")
is_repo = os.path.exists(os.path.join(here, ".git"))

npm_path = os.pathsep.join(
    [
        os.path.join(node_root, "node_modules", ".bin"),
        os.environ.get("PATH", os.defpath),
    ]
)

log.set_verbosity(log.DEBUG)
log.info("setup.py entered")
log.info("$PATH=%s" % os.environ["PATH"])


def js_prerelease(command, strict=False):
    """decorator for building minified js/css prior to another command"""

    class DecoratedCommand(command):
        def run(self):
            jsdeps = self.distribution.get_command_obj("jsdeps")
            if not is_repo and all(os.path.exists(t) for t in jsdeps.targets):
                # sdist, nothing to do
                command.run(self)
                return

            try:
                self.distribution.run_command("jsdeps")
            except Exception as e:
                missing = [t for t in jsdeps.targets if not os.path.exists(t)]
                if strict or missing:
                    log.warn("rebuilding js and css failed")
                    if missing:
                        log.error("missing files: %s" % missing)
                    raise e
                else:
                    log.warn("rebuilding js and css failed (not a problem)")
                    log.warn(str(e))
            command.run(self)
            update_package_data(self.distribution)

    return DecoratedCommand


def update_package_data(distribution):
    """update package_data to catch changes during setup"""
    build_py = distribution.get_command_obj("build_py")
    # distribution.package_data = find_package_data()
    # re-init build_py options which load package_data
    build_py.finalize_options()


class NPM(Command):
    description = "install package.json dependencies using npm"

    user_options = []

    node_modules = os.path.join(node_root, "node_modules")

    targets = [
        os.path.join(here, "glvis", "nbextension", "extension.js"),
        os.path.join(here, "glvis", "nbextension", "index.js"),
        # os.path.join(here, "glvis", "nbextension", "package.json"),
    ]

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def has_npm(self):
        try:
            check_call(["npm", "--version"])
            return True
        except Exception:
            return False

    def run(self):
        if not self.has_npm():
            log.error(
                "`npm` unavailable.  If you're running this command using sudo, make sure"
                "`npm` is available to sudo"
            )
            return

        env = os.environ.copy()
        env["PATH"] = npm_path

        log.info("Installing build dependencies with npm.  This may take a while...")
        check_call(
            ["npm", "install"], cwd=node_root, stdout=sys.stdout, stderr=sys.stderr
        )
        check_call(
            ["npx", "webpack"], cwd=node_root, stdout=sys.stdout, stderr=sys.stderr
        )
        os.utime(self.node_modules, None)

        for t in self.targets:
            if not os.path.exists(t):
                msg = "Missing file: %s" % t
                raise ValueError(msg)

        # update package data in case this created new files
        update_package_data(self.distribution)


version_ns = {}
with open(os.path.join(here, "glvis", "_version.py")) as f:
    exec(f.read(), {}, version_ns)

setup_args = {
    "name": name,
    "version": version_ns["__version__"],
    "description": "Jupyter Widget using glvis-js",
    "long_description": long_description,
    "include_package_data": True,
    "data_files": [
        (
            "share/jupyter/nbextensions/glvis-jupyter",
            [
                "glvis/nbextension/extension.js",
                "glvis/nbextension/index.js",
                "glvis/nbextension/index.js.map",
                # "glvis/nbextension/package.json",
            ],
        ),
        ("etc/jupyter/nbconfig/notebook.d", ["glvis-jupyter.json"]),
    ],
    "install_requires": ["ipywidgets>=7.0.0", "traittypes>=0.2.1"],
    "packages": find_packages(),
    "zip_safe": False,
    "cmdclass": {
        "build_py": js_prerelease(build_py),
        "egg_info": js_prerelease(egg_info),
        "sdist": js_prerelease(sdist, strict=True),
        "jsdeps": NPM,
    },
    "author": "",
    "author_email": "",
    "url": "https://github.com/glvis/pyglvis",
    "keywords": ["ipython", "jupyter", "widgets", "glvis", "mfem"],
    "classifiers": [
        "Framework :: IPython",
        "Topic :: Multimedia :: Graphics",
        "Programming Language :: Python :: 3",
    ],
}

setup(**setup_args)
