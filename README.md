# PCA from First Principles

Mathematical explanations and executable, semantically typed Python examples that build toward principal component analysis. The lectures develop the meaning of mathematical objects and operations before introducing algorithms.

[Read the lectures](https://hafizarslanamjad.github.io/pca-from-first-principles/) · [CI runs](https://github.com/hafizarslanamjad/pca-from-first-principles/actions/workflows/ci.yml)

## Lectures

Lectures 1–6 establish Stage 1 foundations. Lectures 7–8 develop Stage 2: coordinates, reference systems, and matrix representations of reconstruction. Lecture 9 begins Stage 3: observations as data vectors.`

| Lecture | Explanation | Python companion |
| --- | --- | --- |
| 1. Mathematical representation | [Objects, properties, and meaningful numerical relationships](lectures/01-mathematical-representation/index.qmd) | [Labels versus measurements](examples/01_mathematical_representation.py) |
| 2. Scalars and ordered measurements | [Values, feature schemas, and measurement roles](lectures/02-scalars-and-measurements/index.qmd) | [Semantically typed observations](examples/02_scalars_and_measurements.py) |
| 3. Measurements become space | [Feature points, coordinates, and displacement](lectures/03-measurements-become-space/index.qmd) | [Explicit coordinate frames](examples/03_measurements_become_space.py) |
| 4. Vectors, components, and scaling | [Displacements, composition, and scaling](lectures/04-vectors-components-scaling/index.qmd) | [Typed spatial vectors](examples/04_vectors_components_scaling.py) |
| 5. Direction and standard representatives | [Why one representative is useful](lectures/05-direction-and-standard-representatives/index.qmd) | [Typed orientation and amount](examples/05_direction_and_standard_representatives.py) |
| 6. Normalization and algebraic reasoning | [Why division isolates a unit representative](lectures/06-normalization-and-algebraic-reasoning/index.qmd) | [Typed normalization and reconstruction](examples/06_normalization_and_algebraic_reasoning.py) |
| 7. Coordinates and reference systems | [Origins, basis-relative coefficients, and one vector in two bases](lectures/07-coordinates-and-reference-systems/index.qmd) | [Typed coordinates and reconstruction](examples/07_coordinates_and_reference_systems.py) |
| 8. Basis decomposition and matrix multiplication | [Scaled columns, coordinate reconstruction, and inverse questions](lectures/08-basis-decomposition-and-matrices/index.qmd) | [Typed coordinate matrices](examples/08_basis_decomposition_and_matrices.py) |
| 9. Observations as data vectors | [Measurement schemas, feature space, and dataset structure](lectures/09-observations-as-data-vectors/index.qmd) | [Typed observations and dataset layout](examples/09_observations_as_data_vectors.py) |
| 10. Dataset vs feature space | [Why more observations do not add feature dimensions](lectures/10-dataset-and-feature-space/index.qmd) | [Typed counts and feature-wise means](examples/10_dataset_and_feature_space.py) |
| 11. Why do we need a new reference point? | [The mean, deviations, and a change of reference](lectures/11-mean-as-reference/index.qmd) | [Typed centering and reconstruction](examples/11_mean_as_reference.py) |
| 12. What centering changes and preserves | [Reference changes, retained relationships, and broadcasting](lectures/12-centering-reference-change/index.qmd) | [Typed broadcasting and reference checks](examples/12_centering_reference_change.py) |
| 13. Why average deviation fails | [From signed cancellation to population variance](lectures/13-average-deviation-and-variance/index.qmd) | [Typed one-feature spread summaries](examples/13_average_deviation_and_variance.py) |
| 14. Why squaring becomes powerful | [Euclidean decomposition and deviation products](lectures/14-why-squaring-becomes-powerful/index.qmd) | [Typed squared magnitudes and feature products](examples/14_why_squaring_becomes_powerful.py) |
| 15. Relationships between features | [From individual variation to covariance](lectures/15-relationships-between-features/index.qmd) | [Typed covariance examples](examples/15_relationships_between_features.py) |

The [reading-order and conceptual-gap document](docs/stage-1-gap-map.md) explains the prerequisites and where recurring learning questions are addressed. Coverage identifies available explanations; it does not establish demonstrated mastery.

## Scope and status

Lecture 1 establishes the distinction between physical objects and their numerical representations. Its companion demonstrates why identifier differences do not measure physical differences, while subtraction of corresponding measurements has a unit-specific interpretation. Lecture 2 distinguishes scalar values from ordered observations and introduces explicit semantic Python types. Lecture 3 adds typed point, coordinate, and displacement operations with tests of origin-shift invariance and frame compatibility.

Lecture 4 adds a separate spatial-vector model with compatible meter units, directed composition, uniform scaling, and relationship tests. Lecture 5 separates orientation from amount and motivates choosing a unit direction representative. Lecture 6 derives normalization through inverse scaling and explains how algebraic transformations expose a desired relationship. It also distinguishes numerical scale standardization from physical-unit cancellation.

Lecture 7 begins Stage 2 by separating the roles of origins, basis vectors, and coordinate coefficients. It holds one vector fixed while changing its basis representation from `(3, 2)` to `(3, −1)`, explains the negative coefficient through reconstruction, and distinguishes active transformations from passive coordinate changes. Its companion reuses the existing spatial model and represents coefficients together with their basis.

Lecture 8 develops matrix–vector multiplication from a weighted combination of basis-coordinate columns. It derives row-by-column arithmetic, constructs the worked example's inverse from its coordinate equations, and distinguishes a geometric basis from its numerical matrix representation. The companion labels the input and output bases of each coordinate map and checks consistency with Lecture 7.

Lecture 9 constructs length–width observation records before arranging them into a dataset matrix. It distinguishes physical components from feature-space representations, observation positions from signed differences, and observation rows from feature columns. The companion reuses the existing length types and exports an explicitly ordered numerical matrix.

Lecture 10 distinguishes dataset size from feature-space dimension and reproduces the feature-wise means while keeping observation and feature roles explicit. Its source text and notation are preserved with compact paragraph formatting.

Lecture 11 begins Stage 4 by motivating a dataset-derived reference, constructing the mean, and interpreting centered values as signed deviations. The companion retains the reference and observation identifiers for reconstruction. The supplied text is preserved with compact formatting.

Lecture 12 examines centering as a common reference change, verifies preserved pairwise displacements, and connects the operation to row-wise broadcasting. Its coordinate figures are generated with Matplotlib from the numerical examples, and the lecture links directly to both companion and plotting source.

Lecture 13 begins Stage 5 with signed cancellation, mean absolute deviation, and population variance. Its companion preserves the distinction between per-observation deviations and a dataset-level spread summary.

Lecture 14 connects squared magnitude to perpendicular contributions and self-dot-products, distinguishes row and column aggregation, and introduces covariance through products of centered features.

Lecture 15 begins Stage 6 by constructing covariance as an average of signed deviation products. It distinguishes individual contributions from a dataset-level relationship and prepares the covariance matrix.

PCA algorithms and benchmarks are not implemented yet. The Lecture 7 PCA preview introduces the roles of reference directions and observation-specific coefficients; learning those directions and performing dimensionality reduction remain later topics.

## Reproduce the project

The recorded project environment uses Python 3.14.7, Quarto 1.10.18, and uv 0.12.12. These are project versions, not claims about the latest releases. Install Python and Quarto separately, then clone this repository. The commands below use Windows Command Prompt, starting inside the repository root:

```bat
python -m venv .venv
.venv\Scripts\activate.bat
python -m pip install uv==0.12.12
python -m uv sync --locked --extra lectures --extra dev --inexact
set "QUARTO_PYTHON=%CD%\.venv\Scripts\python.exe"
python examples/07_coordinates_and_reference_systems.py
quarto render
quarto preview
```

If `.venv` already exists, activate and synchronize it without recreating it. Stop the preview with Ctrl+C.

On Linux or macOS, activate with `source .venv/bin/activate` and select Python with `export QUARTO_PYTHON="$PWD/.venv/bin/python"`; the remaining Python and Quarto commands are the same.

The local `--inexact` option retains pip and uv installed inside the environment. The established CI workflow installs uv separately and performs exact synchronization. Declare dependency changes in `pyproject.toml` and regenerate `uv.lock` deliberately; do not edit the lockfile by hand.

## Verification and publication

With the project environment activated and `QUARTO_PYTHON` configured, run:

```bat
python -m mypy
python -m pytest
python -m ruff check .
python -m ruff format --check .
quarto render
```

Rendering executes the lecture companions through Quarto and Jupyter. Where a lecture invokes its companion using `runpy.run_path`, the returned namespace is assigned to `_` to suppress notebook expression display while retaining printed output. Script execution alone does not verify this rendering behavior.

Tests cover mathematical relationships and relevant boundary conditions. These include feature-frame compatibility, directed differences, spatial reconstruction, normalization, and Lecture 7's origin shifts and basis-relative reconstruction. The oblique-basis example also checks why summing squared coefficients does not directly give the vector's squared Euclidean magnitude.

The established GitHub Actions workflow checks dependency compatibility, imports, strict type checking, tests, code style, and rendering. Successful builds on `main` deploy to GitHub Pages. Consult the [workflow runs](https://github.com/hafizarslanamjad/pca-from-first-principles/actions/workflows/ci.yml) for actual execution results; the presence of a command or test in the repository does not establish that it has passed.

## Repository layout

| Path | Purpose |
| --- | --- |
| `lectures/` | Quarto lecture sources and supporting assets |
| `examples/` | Executable lecture companions |
| `src/pca_from_first_principles/` | Reusable typed measurement, spatial, normalization, and reference-system operations |
| `tests/` | Mathematical relationship and boundary-condition tests |
| `docs/` | Authoring conventions, reading order, and conceptual-gap guidance |
| `index.qmd` | Website homepage and lecture navigation |
| `_quarto.yml` | Website and rendering configuration |
| `pyproject.toml` and `uv.lock` | Dependency declarations, tool settings, and resolved dependencies |
| `.github/workflows/ci.yml` | Checks, rendering, and deployment |

Work on a short-lived branch, preview changes, and open a pull request into `main`. Add new lectures to the homepage and this table, and update the reading-order document when appropriate. `_quarto.yml` includes lecture pages through its render pattern. Generated `_site/` content and `.venv/` remain outside version control.

## Type checking in the project environment

Mypy is included in the `dev` extra and installed into `.venv`. Run `python -m mypy` locally; the established CI workflow invokes `.venv/bin/python -m mypy` after installing the locked development dependencies. The strict configuration checks `src`, `examples`, and `tests`. Executable code inside `.qmd` is exercised by rendering but is not scanned by this mypy command.

Semantic types distinguish roles such as positions, displacement components, magnitudes, scale factors, direction representatives, and signed basis coefficients. These annotations support static checking; they do not establish physical units or numerical invariants at runtime. Runtime checks separately enforce selected requirements, such as compatible feature frames, finite coefficients, and unit magnitude for direction representatives.

When changing dependency declarations or Python compatibility requirements, update the lockfile and synchronize the environment:

```bat
python -m uv lock
python -m uv sync --locked --extra lectures --extra dev --inexact
python -m mypy --version
python -m mypy
```

Commit the resulting `uv.lock` changes with the dependency update. Locked synchronization intentionally rejects dependency declarations that are inconsistent with the lockfile.

Changes confined to tool settings, such as correcting pytest's `testpaths` from `["test"]` to `["tests"]`, do not require regenerating the dependency lockfile. The Lecture 7 implementation introduces no new dependencies.