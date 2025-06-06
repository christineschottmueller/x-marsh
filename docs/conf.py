# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = 'x-marsh'
copyright = '2025, christine schottmueller'
author = 'christine schottmueller'
release = '0.1.0'

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = []

templates_path = ['_templates']
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']



# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

#html_theme = 'alabaster'
# -- This will hide the project name next to the logo, showing only the image.
html_theme = 'sphinx_rtd_theme'
html_theme_options = {
    'logo_only': True,
    'display_version': False,
}

html_static_path = ['_static']
# -- Link .css file that contains custom font
html_css_files = ['custom.css']

# -- Place logo in the top left corner of theme -----------------------------
html_logo = "_static/logo.png"

html_theme_options = dict(
#html_context = {
  'display_github': True,
  'github_user': 'christineschottmueller',
  'github_repo': 'x-marsh',
  'github_version': '/master/docs/'
}
