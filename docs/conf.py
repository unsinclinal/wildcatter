"""Sphinx configuration."""
project = "Wildcatter"
author = "Geoscience Machine Learning Special Interest Group"
copyright = "2022, Geoscience Machine Learning Special Interest Group"
extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.napoleon",
    "sphinx_click",
    "myst_parser",
]
autodoc_typehints = "description"
html_theme = "furo"
