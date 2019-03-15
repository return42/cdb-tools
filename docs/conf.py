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
    , 'linuxdoc.rstFlatTable'    # Implementation of the 'flat-table' reST-directive.
    , 'linuxdoc.rstKernelDoc'    # Implementation of the 'kernel-doc' reST-directive.
    , 'linuxdoc.kernel_include'  # Implementation of the 'kernel-include' reST-directive.
    , 'linuxdoc.manKernelDoc'    # Implementation of the 'kernel-doc-man' builder
    , 'linuxdoc.cdomain'         # Replacement for the sphinx c-domain.
    #, 'linuxdoc.kfigure'         # Sphinx extension which implements scalable image handling.
]

intersphinx_mapping  = {}
# usage:    :ref:`comparison manual <python:comparisons>`
# intersphinx_mapping['python']  = ('https://docs.python.org/', None)

extlinks = {}
# usage:    :man:`make`
#extlinks['man']       = ('http://manpages.ubuntu.com/cgi-bin/search.py?q=%s', ' ')
#extlinks['rfc']       = ('https://tools.ietf.org/html/rfc%s', 'RFC ')
extlinks['origin']    = ('https://github.com/return42/cdb-tools/blob/master/%s', 'cdb-tools/')
extlinks['commit']    = ('https://github.com/return42/cdb-tools/commit/%s', '#')

html_search_language = 'de'
html_theme           = "sphinx_rtd_theme"
html_logo            = 'darmarIT_logo_128.png'
html_theme_path      = [sphinx_rtd_theme.get_html_theme_path()]
html_static_path     = ["../utils/sphinx-static"]
html_context         = {
    'css_files': [
        '_static/theme_overrides.css', ]
    , }
