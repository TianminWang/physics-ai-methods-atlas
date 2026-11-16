# Maintaining the Atlas · 数据新增与维护

## Core rule

Edit **canonical JSON records**, never hand-edited graph drawings. Every contribution should increase understanding, improve provenance, or make a method easier to locate and learn.

## Adding a paper

1. Search `data/papers/` by title/DOI/arXiv first; **one paper = one record**.
2. Verify authors, title, year, venue and identifiers against the publisher, official proceedings or a trustworthy bibliographic source. Save a `verification_url` and honest status.
3. Create `data/papers/<slug>.json`. Its ID must be `paper.<slug>`.
4. Link the paper to each genuinely relevant method using `data/relations/<slug>.json`, with roles such as `introduces`, `applies`, `analyzes`, `compares` or `surveys`.
5. Update the method's 1–2 `core_reading` selections only if the new paper improves the *minimum reading set*. Add a clear `why` and `focus`.

## Creating a method node

A new node should represent a **distinct, reusable methodological idea or algorithmic framework**. Do not create nodes solely because of a new clinical dataset, task, hyperparameter or small implementation variant.

- Create one `data/methods/<slug>.json`.
- Supply name, summary, central idea, methodological innovation, limitations and the background topics *actually necessary* to learn it.
- Attach at least one area through `belongs_to`.
- Link to relevant problems through `addresses`, without implying those applications validate the method in every clinical setting.
- Use `specializes` for taxonomy, `extends` for evidence-backed methodological extensions, `combines` for evidence-backed mergers. **Never infer ancestry from publication dates alone.**
- Start as `draft`; promote to `curated` only after selecting **1–2 verified linked** must-read papers.

## Books and problems

- A book belongs in `data/books/`; connect to as many methods, areas or problems as genuinely covered via `covers`. Put chapters or sections in the relation's `locator` when available. Books do **not** count toward the per-node paper cap.
- A research task belongs in `data/problems/`; describe observables, unknowns and physical constraints. Attach relevant methods with `addresses`.
- A methodological lineage claim should cite `evidence_paper_ids` and explain the specific innovation or borrowing in the relation `claim`.

## Conventions

- IDs are stable lowercase kebab-case suffixes, e.g. `method.pde-constrained-optimization`.
- Filename equals the ID suffix plus `.json` and must remain stable after publication.
- Relationship records use the legible `source--predicate--target` suffix. The same `(source_id, type, target_id)` triple cannot be duplicated.
- Use `schema_version: "1.0.0"` on every record; change it only through an explicit migration.
- A provisional paper may be stored for research triage, but cannot be the required paper of a curated node.

## Validation and review

~~~bash
python -m pip install -r requirements-dev.txt
python -m scripts.validate
python -m pytest -q
python -m scripts.export_graph
~~~

If validation fails, fix **source records** rather than the derived graph export. Describe **why** new methods deserve nodes and **why** core-reading changes help the learner. Use a feature branch and PR so taxonomic claims, bibliographic metadata and changes to reading burden can be reviewed.

The initial scope prioritizes coronary hemodynamic inverse problems, but the architecture supports other ODE/PDE systems, data assimilation, world models and virtual interventions without needing new entity types for each domain.
