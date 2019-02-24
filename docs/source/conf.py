#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# KUSANAGI SDK for Python documentation build configuration file, created by
# sphinx-quickstart on Fri Jan 2 15:37:32 2019.
#
# This file is execfile()d with the current directory set to its
# containing dir.
#
# If extensions (or modules to document with autodoc) are in another directory,
# add these directories to sys.path here. If the directory is relative to the
# documentation root, use os.path.abspath to make it absolute, like shown here.
#
# import os
# import sys
# sys.path.insert(0, os.path.abspath('.'))
from datetime import datetime
from kusanagi import __version__

# -- General configuration ------------------------------------------------

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.viewcode',
    ]

# Add any paths that contain templates here, relative to this directory.
templates_path = ['_templates']

# The suffix(es) of source filenames.
# You can specify multiple suffix as a list of string:
#
# source_suffix = ['.rst', '.md']
source_suffix = '.rst'

# The master toctree document.
master_doc = 'index'

# General information about the project.
this_year = datetime.now().year
project = 'Python SDK for the KUSANAGI framework'
copyright = '2016-{} KUSANAGI S.L. All rights reserved'.format(this_year)
author = 'Jerónimo Albi'

# The version info for the project you're documenting, acts as replacement for
# |version| and |release|, also used in various other places throughout the
# built documents.
#
# The short X.Y version.
version = __version__.split('-', 1)[0]
# The full version, including alpha/beta/rc tags.
release = __version__

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This patterns also effect to html_static_path and html_extra_path
exclude_patterns = []

# The name of the Pygments (syntax highlighting) style to use.
pygments_style = 'sphinx'

# If true, `todo` and `todoList` produce output, else they produce nothing.
todo_include_todos = False

add_module_names = False
html_show_sphinx = False

# Include both class docstring and __init__
autoclass_content = 'both'

autodoc_default_flags = [
    'members',
    'undoc-members',
    'show-inheritance',
    # 'inherited-members',
    # 'private-members',
    ]

# -- Options for HTML output ----------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
#
html_theme = 'sphinx_rtd_theme'

# Theme options are theme-specific and customize the look and feel of a theme
# further.  For a list of options available for each theme, see the
# documentation.
#
# html_theme_options = {}

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = ['_static']

html_title = 'Release v{}'.format(release)

# -- Options for HTMLHelp output ------------------------------------------

# Output file base name for HTML help builder.
htmlhelp_basename = 'KusanagiSdkForPythonDoc'


# -- Options for manual page output ---------------------------------------

# One entry per manual page. List of tuples
# (source start file, name, description, authors, manual section).
man_pages = [(
    master_doc,
    'kusanagisdkforpython',
    'KUSANAGI Python SDK Documentation',
    [author],
    1,
    )]


# -- Custom code -------------------------------

def remove_module_docstring(app, what, name, obj, options, lines):
    if what == 'module':
        del lines[:]


def mod_signature(app, what, name, obj, options, signature, return_annotation):
    if what != 'module':
        return

    if len(name) > 6:
        return (name[6:], return_annotation)


def setup(app):
    app.connect("autodoc-process-docstring", remove_module_docstring)
    app.connect("autodoc-process-signature", mod_signature)
