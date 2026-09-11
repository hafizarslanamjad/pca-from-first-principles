# PCA from First Principles

Mathematical explanations and executable Python examples that build toward principal component analysis.

[Read the lectures](https://hafizarslanamjad.github.io/pca-from-first-principles/) · [CI runs](https://github.com/hafizarslanamjad/pca-from-first-principles/actions/workflows/ci.yml)

## Lectures

| Lecture | Explanation | Python companion |
| --- | --- | --- |
| 1. Mathematical representation | [Objects, properties, and meaningful numerical relationships](lectures/01-mathematical-representation/index.qmd) | [Labels versus measurements](examples/01_mathematical_representation.py) |

## Scope and status

Lecture 1 establishes the distinction between physical objects and their numerical representations. Its companion demonstrates why identifier differences do not measure physical differences, while subtraction of corresponding measurements has a unit-specific interpretation. PCA algorithms, benchmarks, and mathematical tests are not implemented yet.

## Reproduce the project

The established environment uses Python 3.14.7, Quarto 1.10.18, and uv 0.12.12. Install Python and Quarto separately, then clone this repository. The commands below use Windows Command Prompt, starting inside the repository root:

```bat
python -m venv .venv
.venv\Scripts\activate.bat
python -m pip install uv==0.12.12
python -m uv sync --locked --extra lectures --extra dev --inexact
set "QUARTO_PYTHON=%CD%\.venv\Scripts\python.exe"
python examples/01_mathematical_representation.py
quarto render
quarto preview
```

On Linux or macOS, activate with `source .venv/bin/activate` and select Python with `export QUARTO_PYTHON="$PWD/.venv/bin/python"`; the remaining Python and Quarto commands are the same. Stop the preview with Ctrl+C.

The local `--inexact` option retains pip and uv installed inside the environment. CI installs uv separately and performs exact synchronization. Commit dependency changes through `pyproject.toml` and regenerate `uv.lock` deliberately; do not edit the lockfile by hand.

## Verification and publication

```bat
python -m ruff check .
python -m ruff format --check .
quarto render
```

Rendering executes the lecture's Python companion from the same script used at the command line. GitHub Actions checks dependency compatibility, imports, code style, and rendering. Successful builds on `main` deploy to GitHub Pages. Mathematical tests will be added with implementations that have mathematical behavior to verify.

## Repository layout

| Path | Purpose |
| --- | --- |
| `lectures/` | Quarto lecture sources |
| `examples/` | Executable companions |
| `src/pca_from_first_principles/` | Package reserved for reusable implementations |
| `pyproject.toml` and `uv.lock` | Dependency declarations and resolved versions |
| `.github/workflows/ci.yml` | Checks, rendering, and deployment |

Work on a short-lived branch, preview changes, and open a pull request into `main`. Add new lectures to the homepage and this table. `_quarto.yml` includes lecture pages through its render pattern. Generated `_site/` content and `.venv/` remain outside version control.
