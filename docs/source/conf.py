# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = 'Ansible for Network Automation'
copyright = '2024, Syed Asif'
author = 'Syed Asif'

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = [
        "myst_parser",
        "sphinx.ext.duration",
        "sphinx.ext.autosectionlabel",
        "sphinx.ext.autodoc",
        ]





# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = "sphinx_book_theme"
html_static_path = ['_static']

# -- Options for LaTeX/PDF output -------------------------------------------
# Map the Unicode glyphs used in shell-prompt / directory-tree code blocks
# to LaTeX equivalents so pdflatex can compile the book.
latex_elements = {
    'preamble': r'''
\DeclareUnicodeCharacter{2500}{-}  % ─  box-drawing horizontal
\DeclareUnicodeCharacter{2502}{|}  % │  box-drawing vertical
\DeclareUnicodeCharacter{251C}{+}  % ├  box-drawing tee
\DeclareUnicodeCharacter{2514}{+}  % └  box-drawing elbow
\DeclareUnicodeCharacter{279C}{$\rightarrow$}  % ➜  heavy arrow (prompt)
\DeclareUnicodeCharacter{2717}{$\times$}       % ✗  ballot cross
'''
}
