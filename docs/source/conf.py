# Configuration file for the Sphinx documentation builder.

import platform
from datetime import datetime
from zoneinfo import ZoneInfo
import sphinx
import sphinx_material

# -- Project information

project = 'SPUIS'
copyright = '2023, Eijk van der'
author = 'Martin van der Eijk'
release = "0.1.0"
now = datetime.now(tz=ZoneInfo("Europe/Paris"))
version = f"{now.year}-{now.month:02}-{now.day:02} {now.hour:02}H ({now.tzinfo})"
today = version

# -- General configuration
extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.doctest",
    "sphinx.ext.extlinks",
    "sphinx.ext.intersphinx",
    "sphinx.ext.todo",
    "sphinx.ext.mathjax",
    "sphinx.ext.viewcode",
    "sphinx_copybutton",
]

intersphinx_mapping = {
    'python': ('https://docs.python.org/3/', None),
    'sphinx': ('https://www.sphinx-doc.org/en/master/', None),
}
intersphinx_disabled_domains = ['std']

templates_path = ['_templates']

# -- Options for HTML output

html_theme = 'sphinx_rtd_theme'

# -- Options for EPUB output
epub_show_urls = 'footnote'
