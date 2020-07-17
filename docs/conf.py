# -*- coding: utf-8; mode: python -*-
#
# Sphinx documentation build configuration file

import os, sys
sys.path.insert(0, os.path.abspath(os.path.join("..", "lib")))
from dm import __pkginfo__ as pkginfo

from pallets_sphinx_themes import ProjectLink

GIT_URL  = 'https://github.com/return42/cdb-tools'
DOCS_URL = 'https://return42.github.io/cdb-tools'

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

jinja_contexts = {}

extlinks = {}
# usage:    :man:`make`
#extlinks['man']      = ('http://manpages.ubuntu.com/cgi-bin/search.py?q=%s', ' ')
#extlinks['rfc']      = ('https://tools.ietf.org/html/rfc%s', 'RFC ')
extlinks['origin']    = (GIT_URL + '/blob/master/%s', 'cdb-tools/')
extlinks['commit']    = (GIT_URL + '/commit/%s', '#')
extlinks['wiki']      = (GIT_URL + '/wiki/%s', ' ')
extlinks['pull']      = (GIT_URL + '/pull/%s', 'PR ')
extlinks['docs']      = (DOCS_URL + '/%s', 'docs: ')
extlinks['pypi']      = ('https://pypi.org/project/%s', 'PyPi: ')

extensions = [
    'sphinx.ext.imgmath',
    'sphinx.ext.extlinks',
    "sphinx.ext.autodoc",
    "sphinx.ext.coverage",
    "sphinx.ext.intersphinx",
    "sphinx.ext.todo",
    "pallets_sphinx_themes",
    "sphinx_issues", # https://github.com/sloria/sphinx-issues/blob/master/README.rst
    "sphinxcontrib.jinja",  # https://github.com/tardyp/sphinx-jinja
    "sphinxcontrib.programoutput",  # https://github.com/NextThought/sphinxcontrib-programoutput
    'linuxdoc.kernel_include',  # Implementation of the 'kernel-include' reST-directive.
    'linuxdoc.rstFlatTable',    # Implementation of the 'flat-table' reST-directive.
    'linuxdoc.kfigure',         # Sphinx extension which implements scalable image handling.
    "sphinx_tabs.tabs", # https://github.com/djungelorm/sphinx-tabs
]

intersphinx_mapping = {
    "python": ("https://docs.python.org/3/", None),
    "flask": ("https://flask.palletsprojects.com/", None),
    # "werkzeug": ("https://werkzeug.palletsprojects.com/", None),
    "jinja": ("https://jinja.palletsprojects.com/", None),
    "linuxdoc" : ("https://return42.github.io/linuxdoc/", None),
    "sphinx" : ("https://www.sphinx-doc.org/en/master/", None),
}

issues_github_path = "return42/cdb-tools"

# HTML -----------------------------------------------------------------

sys.path.append(os.path.abspath('_themes'))
html_title = "CDB-Tools ({})".format(pkginfo.version)
html_logo = 'darmarIT_logo_128.png'
html_search_language = 'de'
html_show_sourcelink = False

html_theme_path = ['_themes']
html_theme = "cdb-tools"
html_static_path = ["static"]

# sphinx.ext.imgmath setup
html_math_renderer = 'imgmath'
imgmath_image_format = 'svg'
imgmath_font_size = 14
# sphinx.ext.imgmath setup END

html_theme_options = {"index_sidebar_logo": True}
html_context = {
    "project_links": [
        ProjectLink("Source", GIT_URL),
        ProjectLink("Get git started", 'http://return42.github.io/handsOn/slides/git'),
        ProjectLink("CDB Entwicklung", 'slides/cdb_comp/index.html'),
    ]
}

if todo_include_todos:
    html_context['project_links'].append(ProjectLink("ToDo", '/todo.html'))

html_sidebars = {
    "**": ["project.html", "relations.html", "searchbox.html"],
}
singlehtml_sidebars = {"index": ["project.html", "localtoc.html"]}
