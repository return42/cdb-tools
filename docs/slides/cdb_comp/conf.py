# -*- coding: utf-8 -*-
#
# Sphinx documentation build configuration file

import os, sys
sys.path.insert(0, os.path.abspath(os.path.join("..", "..", "..", "lib")))

from dm import __pkginfo__ as pkginfo

language  = 'de'
project   = u'CDB Komponenten Architektur'
copyright = pkginfo.copyright
version   = pkginfo.version
release   = pkginfo.version
author    = pkginfo.authors[0]

source_suffix       = '.rst'
show_authors        = True
master_doc          = 'index'

# -- Options for HTML output --------------------------------------

extensions = [
    'sphinxjp.themes.revealjs'
    , 'sphinx.ext.intersphinx'
    , 'linuxdoc.kfigure'         # Sphinx extension which implements scalable image handling.
]

intersphinx_mapping  = {}
# usage:    :ref:`comparison manual <python:comparisons>`
# intersphinx_mapping['python']  = ('https://docs.python.org/', None)

extlinks = {}
# usage:    :man:`make`
extlinks['man']       = ('http://manpages.ubuntu.com/cgi-bin/search.py?q=%s', ' ')
extlinks['origin']    = ('https://github.com/return42/cdb-tools/blob/master/%s', 'cdb-tools/')
extlinks['commit']    = ('https://github.com/return42/cdb-tools/commit/%s', '#')

html_theme = 'revealjs'
html_use_index = False

# -- HTML theme options for `revealjs` style ---------------------

html_theme_options = {

    # Set the lang attribute of the html tag. Defaults to "ja"
    'lang': 'de',

    # Theme (black/white/league/beige/sky/night/serif/simple/solarized/dejavu)
    'theme': 'dejavu',

    # Transition style (default(=convex)/none/fade/slide/concave/zoom)
    'transition': 'slide',

    # Display the page number of the current slide
    'slide_number': True,

    # Enable plguin javascript for reveal.js
    # "plugin_list": [
    #  "_static/plugin/search/search.js",
    #  "_static/plugin/remotes/remotes.js"
    # ],

    # config for Multiplexing
    # "multiplex": {
    #   # None so the clients do not have control of the master presentation
    #   "secret": None,
    #   "id": '1ea875674b17ca76', # id, obtained from socket.io server
    #   "url": 'example.com:80' # Location of your socket.io server
    # },

    # loading custom js after RevealJs.initialize.
    "customjs": "mysettings.js",

    # loading custom css
    "customcss": "mysettings.css",
}

html_static_path = ['_static']
