# Maintaining the Atlas · 数据新增与维护

## Editing principle

Edit **canonical JSON files**; never manually edit generated graph drawings or copies of a paper record. Method names, claims, reference roles and study suggestions must stay distinct.

## New paper

1. Look for duplicates by **DOI, arXiv identifier and title** in `data/papers/`.
2. Verify original author list, publication venue, date, and persistent identifier through the publisher, proceedings, or trusted bibliographic source. Store a `verification_url`; `provisional` is permitted when not fully checked.
3. Create `data/papers/<slug>.json` with `schema_version: "2.0.0"`. **Do not add a global `landmark` flag.**
4. Connect the paper to one or more relevant methods using typed paper→method relations: `introduces`, `analyzes`, `applies`, `compares`, or `surveys`. The same paper can serve different roles for different methods.
5. Put `significance: "landmark"` **on the specific paper→method relation** only when the contribution is demonstrably foundational or a major turning point **for that method**. Explain via `significance_reason`. `representative` and `supporting` are alternatives, not ranks of the entire paper.
6. Optionally add the source to a method's `start_here` recommendations **only** when it efficiently teaches that method. Typical goal is 1–2, but there is **no minimum or maximum**.

## New method

A method node should capture a reusable and conceptually distinct algorithm, formulation or framework. Do not turn every new application, benchmark, clinical cohort, hyperparameter tweak or paper into a new node.

- Create `data/methods/<slug>.json` with a stable ID, short `summary`, `core_idea`, `innovation`, `limitations`, `background_topics`, and `status`.
- Link to its navigational areas with `belongs_to`, and to scientific tasks with `addresses`.
- `specializes` is a taxonomic claim; `extends` is evidence-backed methodological modification; `combines` is evidence-backed multi-method fusion; `depends_on` means a **learning** prerequisite. Do not blur these relations.
- A `curated` method has a reviewed definition and sufficiently checked claims; it need **not** have any `start_here` items. A `draft` is still under scholarly review. Both may have references.
- If recommendations are included, write `reference_id` (paper or book), `why`, `focus`, optionally `locator` and a documented publication-status exception. **All recommendations are advisory**, not an obligation to the reader.
- Every recommended paper must be verified and have a paper→method relation; each recommended book must have a `covers` relation to the method.

## Books and problems

- Create `data/books/<slug>.json`; books may cover multiple methods/areas/problems via `covers`, with a chapter/section `locator` when known. A textbook chapter is often a better first reference for a historic method than a difficult original primary source.
- Create `data/problems/<slug>.json` for a scientific problem, listing actual unknowns, available observations and model constraints.
- `addresses` means an applicable methodological tool subject to assumptions, **not** proof of clinically validated performance.
- Never equate evidence from a **systemic 1D vascular network** directly to a coronary 3D patient-specific validation claim.

## ID/version conventions

- All files contain `schema_version: "2.0.0"`.
- The file's stem must match the ID suffix (`method.fno` → `data/methods/fno.json`).
- Use stable lowercase kebab-case slugs; avoid renaming IDs after there are inbound links.
- Relations use `source--predicate--target` slugs. The triple `(source_id, type, target_id)` must be unique.
- Lineage edges (`extends`, `combines`) require evidence paper IDs; their chronological order and specific causal/methodological claim deserve manual scholarly review.

## Local checks and PR review

~~~bash
python -m pip install -r requirements-dev.txt
python -m scripts.validate
python -m pytest -q
python -m scripts.export_graph
~~~

Validation enforces structural integrity, not the correctness of a scientific theorem. For each new method or lineage link, manually inspect the cited scientific source and state the boundary of its evidence. For changes to `start_here`, explain why the new recommendation reduces the reader's effort or adds key conceptual coverage. Prefer a feature branch/PR so changes are reviewable.

The atlas should help prioritize research about PDE/ODE inverse problems, coronary hemodynamics and future digital twins. It does not impose a separate full mathematics curriculum or assume the user will read every paper.
