# Lecture authoring conventions

Keep related reasoning in continuous paragraphs. Use inline mathematics for short values and expressions; reserve display equations for derivations that benefit from their own line. Avoid artificial one-sentence paragraphs, oversized prose equations, and unnecessary table padding. Preserve readable mathematical notation and conventional Python formatting.

Give variables explicit semantic roles in their annotations. Distinguish storage types such as float or an array from roles such as measured mass, observation, coordinate, mean, basis vector, or difference. Introduce only roles justified by the current lecture. Do not give a coordinate or vector label to a record before explaining that interpretation.

Use NewType when distinct scalar roles should be checked statically, and named records when ordering, fields, or whole-observation identity matter. A plain type alias is a readable synonym, not a distinct type. Explain what annotations guarantee and what they do not: runtime unit conversion, shape validation, frame compatibility, finiteness, and geometric invariants require additional design. A static checker must actually be run; Ruff is not that checker.

State the reference and result meaning for operations. In particular, distinguish observations from signed differences and specify target minus reference. Preserve units through each component operation. Introduce mean, coordinate, and basis types with their relevant spaces, feature schema, or frames when those concepts arrive.

Execute each lecture's companion from its source file during Quarto rendering, so printed output and standalone code agree. Add meaningful mathematical tests when reusable operations are introduced, and make validation claims only for checks actually run.

Install mypy inside the project virtual environment through the dev extra. Run `python -m mypy` locally and the matching environment-specific command in CI. Keep its version in uv.lock; regenerate the lockfile whenever development dependencies change. Do not use a separate uv tool environment for project type checking.
