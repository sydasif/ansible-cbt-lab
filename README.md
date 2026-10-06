# Ansible-cbt-lab

Ansible network automation lab with GNS3 and Cisco devices, plus the companion book *Ansible for Network Automation* (sources in `docs/`, built with Sphinx + MyST Markdown).

**Hosted version:** <https://ansible-cbt-lab.readthedocs.io/en/latest/> — Read the Docs rebuilds the HTML, PDF and ePub automatically on every push (see `.readthedocs.yaml`).

## Building the PDF book locally

### Prerequisites

System packages (TeX Live for LaTeX, `latexmk` to drive it):

```bash
sudo apt-get update
sudo apt-get install texlive-xetex texlive-fonts-recommended texlive-plain-generic
sudo apt install latexmk
```

Python environment (Sphinx, MyST Markdown parser, book theme):

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

> Note: `pandoc` is **not** required for this build. The pipeline is
> `sphinx-build` (MyST parses the Markdown natively) → `latexmk` → `pdflatex`.

### Build

```bash
source .venv/bin/activate
cd docs
make latexpdf
```

Output: `docs/_build/latex/ansiblefornetworkautomation.pdf`
(the filename is derived from the `project` name in `docs/source/conf.py`).

Copy it next to the other local artifacts:

```bash
cp _build/latex/ansiblefornetworkautomation.pdf ../my_book/
```

### HTML preview

```bash
cd docs
make html          # open docs/_build/html/index.html
```

### Unicode glyphs in code blocks

Shell prompts and directory trees in the chapters use non-ASCII characters
(`➜`, `✗`, `─`, `├`, `└`, `│`). pdflatex only knows these because of the
`latex_elements` preamble in `docs/source/conf.py`, which maps each one to a
LaTeX equivalent. **If you add a new non-ASCII character to a code block, add a
matching `\DeclareUnicodeCharacter{...}{...}` line there**, otherwise the PDF
build fails with `LaTeX Error: Unicode character ... not set up for use with LaTeX`.

