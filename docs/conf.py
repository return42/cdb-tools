# -*- coding: utf-8; mode: python -*-
#
# Sphinx documentation build configuration file

import os, sys
sys.path.insert(0, os.path.abspath(os.path.join("..", "lib")))

from dm import __pkginfo__ as pkginfo
import sphinx_rtd_theme

language  = 'de'
project   = 'CDB Tools'
copyright = pkginfo.copyright
version   = pkginfo.version
release   = pkginfo.version
author    = pkginfo.authors[0]

source_suffix       = '.rst'
show_authors        = True
master_doc          = 'index'
templates_path      = ['_templates']
exclude_patterns    = ['_build', 'slides']
todo_include_todos  = True

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

intersphinx_mapping  = {}
# usage:    :ref:`comparison manual <python:comparisons>`
# intersphinx_mapping['python']  = ('https://docs.python.org/', None)

extlinks = {}
# usage:    :man:`make`
#extlinks['man']       = ('http://manpages.ubuntu.com/cgi-bin/search.py?q=%s', ' ')
#extlinks['rfc']       = ('https://tools.ietf.org/html/rfc%s', 'RFC ')

html_search_language = 'de'
html_theme           = "sphinx_rtd_theme"
html_logo            = 'darmarIT_logo_128.png'
html_theme_path      = [sphinx_rtd_theme.get_html_theme_path()]
html_static_path     = ["../utils/sphinx-static"]
html_context         = {
    'css_files': [
        '_static/theme_overrides.css', ]
    , }
