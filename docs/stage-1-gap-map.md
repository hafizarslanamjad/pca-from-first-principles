# Stage 1: Reading Order and Conceptual Gaps

Stage 1 develops the foundations needed before studying PCA. The reading order follows conceptual prerequisites rather than the chronological order of the original conversations. Questions raised during learning are incorporated where their explanations belong. This document also identifies how Lecture 7 carries these foundations into Stage 2.

## Lectures 1–3: Representation, Measurements, and Space

Lecture 1 distinguishes an object from its mathematical representation. Lecture 2 introduces scalar measurements, ordered observations, and the semantic roles of their entries. Lecture 3 develops feature spaces, points, coordinates, reference frames, and displacement. Together, these lectures establish why a numerical list needs an interpretation before its entries and operations become meaningful.

## Lecture 4: What Exactly Is a Vector?

Lecture 4 follows the learner-selected text from the original Stage 1, Part 4: sections 1–5 and 7–9. The original section numbers are preserved. Section 6, which introduced normalization before its prerequisites were sufficiently explained, is intentionally omitted from this selection.

The lecture moves from points and displacement to computational representations, vector addition, scalar multiplication, basis directions, coordinate descriptions, and feature-space differences. Its central distinction is between a geometric vector and the coordinates used to represent it under a chosen basis.

## Lecture 5: Direction and Its Standard Vector Representative

Lecture 5 addresses why numbers can represent a direction without implying that direction itself inherently has an amount. It begins with signs and displacement on a number line, then extends the reasoning to different vectors sharing the same direction in two dimensions.

The lecture distinguishes direction, directed displacement, and coordinate representation. It explains why mathematics benefits from choosing a standardized representative and why magnitude one makes the scaling coefficient directly express the amount. It ends by establishing the multiplication relationship that the next lecture will reverse.

## Lecture 6: Normalization and the Reasoning Behind Algebraic Steps

Lecture 6 derives normalization as reciprocal scalar multiplication. It explains how division reverses a known scaling operation, why dividing by magnitude produces a unit representative, and which properties the operation preserves.

The scaling derivation also develops goal-directed algebraic reasoning: identify the desired relationship, find a known expression that represents it, and choose equality-preserving transformations that expose that expression. Expansion reveals the common scale factor, factoring reveals the old squared magnitude, substitution names that quantity, and taking the nonnegative square root completes the relationship between magnitudes.

The bananas analogy connects normalization to factor isolation. The lecture distinguishes scale standardization from physical-unit cancellation and explains why retaining both magnitude and the unit representative permits reconstruction of the original vector.

## Lecture 7: Coordinates and Reference Systems — Stage 2 Begins

[Lecture 7 — Coordinates and Reference Systems](../lectures/07-coordinates-and-reference-systems/index.qmd) begins Stage 2 by asking what a coordinate is relative to. The road-and-tree example establishes the roles of origin, orientation, and unit: changing the origin changes the tree's coordinate without moving the tree.

The lecture then separates the reference requirements of points and free vectors. A point's coordinates depend on an origin and a basis, while a free vector's coordinates depend on the basis. Translating the origin with the basis held fixed changes point coordinates but preserves the coordinate differences representing displacement.

Coordinates are developed as signed reconstruction coefficients relative to an ordered basis. The worked example holds `v = 3e₁ + 2e₂` fixed and introduces `p₁ = e₁ + e₂` and `p₂ = e₂`. Substitution, distribution, grouping, and comparison in the original basis establish `v = 3p₁ − p₂`. The coordinate column changes from `(3, 2)` to `(3, −1)` while the represented vector stays the same.

The negative coefficient is explained geometrically: three copies of `p₁` contribute one extra upward step, which one copy of `−p₂` removes. The example also establishes that basis vectors need not be unit vectors or perpendicular. Consequently, coefficients in this oblique basis cannot be inserted directly into the familiar sum-of-squares magnitude formula.

The lecture concludes by distinguishing active transformations from passive changes of coordinates. Its PCA preview separates learned reference directions from observation-specific coefficients and distinguishes complete coordinate representations from later dimensionality reduction.

## Lecture 8: From Basis Decomposition to Matrix Multiplication

[Lecture 8 — From Basis Decomposition to Matrix Multiplication](../lectures/08-basis-decomposition-and-matrices/index.qmd) packages Lecture 7's reconstruction relationship as a matrix–vector product. It distinguishes the geometric basis P from the matrix A whose columns contain that basis's coordinates in E, giving `[v]_E = A[v]_P`.

The lecture first interprets multiplication as a weighted combination of columns, then derives row-by-column arithmetic by collecting contributions to each output coordinate. It reverses the question to extract coordinates and constructs the example's inverse from the equations already derived. The orthonormal inverse–transpose relationship is introduced as a later connection requiring dot-product and projection reasoning, rather than treated as established understanding.

## Lecture 9: Observations as Data Vectors — Stage 3 Begins

[Lecture 9 — Observations as Data Vectors](../lectures/09-observations-as-data-vectors/index.qmd) begins with physical components and an ordered length–width measurement schema. It constructs observation vectors, gives feature axes explicit numerical meanings, and distinguishes those axes from spatial directions. Matching-feature subtraction produces a signed difference rather than another absolute observation.

The four supplied observations become rows of a dataset matrix through explicit transposition of their column representations. Rows hold observations fixed; columns hold features fixed. The lecture preserves the distinction between selected information and the full physical object, and ends before centering. The next topic is the distinction between the dataset and its ambient feature space.

## Lecture 10: Dataset vs Feature Space

[Lecture 10 — Dataset vs Feature Space](../lectures/10-dataset-and-feature-space/index.qmd) distinguishes n observations from d feature coordinates, compares aggregation across observations with aggregation across features, and introduces the distinction between ambient representation size and the structure occupied by the data. It preserves the supplied examples and notation. The next question is the mean as a common reference and centering as a reference change.

## Conceptual Gap Map

The entries below identify where explanations are provided. They are a reading guide, not a record of demonstrated mastery.

| Question raised during learning | Where it is addressed |
| --- | --- |
| How does a mathematical representation differ from the object represented? | Lectures 1–3; revisited for vectors in Lecture 4 and changing references in Lecture 7 |
| Why is a list of numbers not enough to specify a vector's meaning? | Lecture 4; Lecture 7 makes the basis-dependent meaning of each entry explicit |
| How do points, displacements, bases, and coordinates differ? | Lectures 3–4; their separate reference requirements are developed in Lecture 7 |
| What does vector magnitude represent, and what information does it omit? | Lecture 5; revisited through extraction and reconstruction in Lecture 6 |
| Why can numbers represent direction when signs seemed sufficient on a line? | Lecture 5 |
| How can vectors of different magnitudes share one direction? | Lecture 5 |
| Why choose one standard representative, and why give it magnitude one? | Lecture 5 |
| Why does scaling a unit vector by five produce magnitude five? | Lecture 5; derived explicitly and generalized in Lecture 6 |
| Why divide by magnitude, and what operation does that division represent? | Lecture 6 |
| How does the bananas analogy explain factor isolation? | Lecture 6; Lecture 7 reconnects factor roles to reconstruction coefficients |
| Are normalized components fractions that must add to one? | Lectures 5–6: unit magnitude requires the sum of squared components to equal one in the stated orthonormal Euclidean setting |
| What happens to physical units during normalization? | Lecture 6, building on the measurement distinctions in earlier lectures |
| How do we decide which algebraic transformation to perform next? | Lecture 6; applied to substitution, grouping, and coefficient isolation in Lecture 7 |
| What information is lost through magnitude extraction or normalization? | Lecture 6 |
| How can the original vector be reconstructed from magnitude and direction? | Lecture 6 |
| Can the zero vector be normalized? | Lectures 5–6: it has no unique direction and cannot be divided by its zero magnitude |
| What is a position coordinate relative to? | Lecture 7: origin, reference orientation, and scale |
| How can a coordinate change when the point has not moved? | Lecture 7: the road-and-tree origin shift |
| Why does changing the origin preserve displacement between fixed points? | Lecture 7: the common coordinate shift cancels when differences are taken |
| What do the entries of a vector's coordinate column mean? | Lecture 7: signed coefficients multiplying the ordered basis vectors |
| Why can one vector have different coordinates in different bases? | Lecture 7: the explicit change from basis E to basis P |
| Why can changing the basis introduce a negative coordinate? | Lecture 7: removing the extra upward contribution of three copies of p₁ |
| Why is comparing coefficients valid in the worked derivation? | Lecture 7: independence of the basis vectors gives unique coefficients |
| Must basis vectors be unit length and perpendicular? | Lecture 7: the oblique basis provides a counterexample |
| Why does the usual sum of squared coordinates fail in the oblique basis? | Lecture 7: its coefficients are not components along perpendicular unit vectors |
| How does changing an object differ from changing its representation? | Lecture 7: active transformations and passive changes of coordinates |
| How do PCA reference directions differ from observation-specific coefficients? | Lecture 7 introduces their semantic roles; their construction and calculation remain for later lectures |
| Does a complete change of basis discard information? | Lecture 7: all coefficients together with the basis permit reconstruction; retaining fewer directions is a separate operation |
| How does basis decomposition become matrix–vector multiplication? | Lecture 8: package reference-coordinate columns and their matching coefficients |
| Why are reference representations placed in columns? | Lecture 8: the column-vector convention aligns each coefficient with a complete reference column |
| Where does row-by-column arithmetic come from? | Lecture 8: collect the scaled columns' contributions to each output coordinate |
| How does a geometric basis differ from its numerical matrix? | Lecture 8: P names the basis; A stores its coordinate columns relative to E |
| How does coordinate extraction reverse reconstruction? | Lecture 8: derive the inverse map from the coordinate equations |
| When can transpose replace inverse? | Lecture 8 states the square orthonormal case and gives an oblique counterexample; geometric justification remains for later dot-product work |
| How does a physical object become a data vector? | Lecture 9: select features, define the schema, then collect values |
| How do feature axes differ from physical directions? | Lecture 9: numerical length–width feature coordinates |
| What does subtracting two observation representations mean? | Lecture 9: target minus reference in matching features |
| Why do column-form observations become dataset rows? | Lecture 9: explicit transposition under an observations-by-features convention |
| How do an observation vector and a feature column differ? | Lecture 9: fix one observation versus one feature |
| What information is discarded before learning begins? | Lecture 9: measurement selection versus value-preserving matrix organization |

| Why do more observations not add feature dimensions? | Lecture 10: n counts observations; d counts descriptive slots |
| How do averaging axes change the question? | Lecture 10: preserve feature identity or combine features within one observation |
| Does d stored features imply d independent variations? | Lecture 10: thickness tied to length retains a third slot but constrains the data |

## Assumptions to Carry Forward

The Stage 1 spatial magnitude and normalization examples use perpendicular, equally scaled axes with compatible units. These examples do not justify treating length and mass as interchangeable quantities or adding their squares to obtain a physical distance. Choosing a metric or scaling heterogeneous features remains a modeling question to revisit when developing PCA.

Notation distinguishes a geometric vector `v`, its coordinate representation `[v]_E` under the ordered basis `E`, its magnitude `‖v‖`, and its unit direction representative `u`. A unit direction representative is dimensionless in the physical displacement examples; the magnitude carries the physical unit.

For a real scalar `a`, the magnitude relationship is `‖av‖ = |a| ‖v‖`. Positive scaling preserves direction, negative scaling reverses it, and zero scaling produces the zero vector. Magnitude and a unit representative together reconstruct a nonzero vector; either piece alone loses information.

Lecture 7 uses `Q` for a geometric point and `P = (p₁, p₂)` for the alternative basis. Point coordinates require an origin as well as a basis. The abbreviated notation `[Q]_O` assumes that orientation and units remain fixed; the fuller notation `[Q]_(O,E)` makes both origin and basis explicit. A free vector's basis representation `[v]_E` does not require a separate origin.

A basis vector has a scale as well as an orientation. Coordinates specify signed multiples of the actual basis vectors, so a coefficient's absolute value equals the magnitude of its individual contribution only when the corresponding reference vector has unit magnitude in the stated model. In Lecture 7, `p₁ = e₁ + e₂` has magnitude `√2`, and the alternative basis is oblique. It must not be treated as an orthonormal basis.

The Lecture 7 derivation first uses a dimensionless numerical model, then explicitly restores meters for the Python companion. The existing `SpatialVector` stores displacement components in the fixed orthonormal spatial frame; the new coordinate representation records signed coefficients together with their basis. Static annotations express these roles, while runtime checks enforce selected numerical invariants rather than a general physical-units system.

## Continuing Stage 3

Lectures 4–6 cover the planned Stage 1 material on vectors, direction representatives, normalization, and the reasoning behind the associated algebra.

Lecture 7 begins Stage 2 with origins, basis-relative coordinates, and a worked change of basis. Lecture 8 expresses that reconstruction through matrix multiplication and derives the reverse coordinate map for the same example.

Lecture 9 now begins Stage 3 with observations and dataset layout. Dataset size versus feature-space dimension remains the next question, before mean-based centering. Coverage does not establish demonstrated mastery.

Subsequent lectures can develop why dot products and projections extract coefficients in orthonormal bases and how reference directions are selected in PCA. Lecture 8 introduces the relevant inverse–transpose identity, but its geometric justification still requires its own development.

Each new derivation should state its goal, explain why its transformations serve that goal, and identify what information is preserved or discarded. Coverage of a topic does not establish permanent mastery; earlier explanations should be revisited when a new application exposes another gap.

Lecture 10 covers the dataset-size versus feature-dimension question anticipated in Lecture 9. The transition now leads to Stage 4: the mean as a reference point. Coverage remains distinct from demonstrated mastery.
