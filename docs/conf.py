# -*- coding: utf-8; mode: python -*-
#
# Sphinx documentation build configuration file

import os, sys
sys.path.insert(0, os.path.abspath(os.path.join("..")))

import dm
import sphinx_rtd_theme

master_doc = 'index'
templates_path = ['_templates']
exclude_patterns = ['_build', 'slides']

project   = 'CDB Tools'
copyright = dm.__copyright__
version   = dm.__version__
release   = dm.__version__
show_authors = True

extensions = [
    'sphinx.ext.autodoc'
    , 'sphinx.ext.extlinks'
    #, 'sphinx.ext.autosummary'
    #, 'sphinx.ext.doctest'
    , 'sphinx.ext.todo'
    , 'sphinx.ext.coverage'
    #, 'sphinx.ext.pngmath'
    #, 'sphinx.ext.mathjax'
    , 'sphinx.ext.viewcode'
    , 'sphinx.ext.intersphinx'
]

html_theme = "sphinx_rtd_theme"
html_theme_path = [sphinx_rtd_theme.get_html_theme_path()]
html_static_path = ["../utils/sphinx-static"]
html_context = {
    'css_files': [
        '_static/theme_overrides.css',
    ],
}

intersphinx_mapping = {}
html_logo = 'darmarIT_logo_128.png'
