# Roadmap · 项目计划与完成标准

## Phase 1 — Foundational schema and validation (completed; refined in v0.2)

- [x] Single canonical source for Method, Paper, Book, Problem, Area and typed Relation records.
- [x] Evidence provenance, stable IDs, cross-file reference and typed-edge checks, DAG checks for specified graph projections.
- [x] Make `start_here` a **nonbinding, uncapped advisory reading suggestion**, not a mandatory 1–2 quota.
- [x] Attach `landmark` significance to contextual **paper→method contributions**, never a global yes/no paper tag.
- [x] Allow book chapters alongside papers in recommended starting references.
- [x] Deterministic graph export, regression tests and GitHub Actions validation.
- [x] Document curation, methodology and data compatibility (`schema_version: 2.0.0`).

## Phase 2 — Initial curated methods and literature (v0.2)

- [x] Construct classical inverse-theory spine: nonlinear least squares, Gauss–Newton, LM, Tikhonov, adjoint gradients, PDE-constrained optimization, Bayesian inverse problems.
- [x] Construct scientific ML spine: PINN, neural operators, DeepONet, FNO, PINO / physics-informed DeepONet, learned-forward inversion, direct inverse operator, DINO and geometry-adaptive operators.
- [x] Add data assimilation, ROM/operator inference and hemodynamics boundary-model branches.
- [x] Link high-priority original works, syntheses, selected books and relevant coronary/systemic vascular tasks.
- [x] Add minimal-reading guide and systematic, provenance-aware paper→method roles.
- [ ] Continue scholarly curation as a living project: fuller author/DOI audits, comparative critiques, and underrepresented research branches. **No static literature collection is ever complete.**

**Scope of v0.2:** 30 method records, 32 paper/chapter records, 8 books, 10 problems and 5 areas linked by 210 typed relationships. These numbers measure the current indexed scope, not exhaustive coverage.

## Phase 3 — Interactive knowledge graph (planned, NOT yet done)

- [ ] GitHub Pages for a searchable, filterable default **method-evolution forest (A)**.
- [ ] Switchable **research problem / digital-twin pipeline (B)** view, plus optional **learning prerequisites (C)**.
- [ ] Click methods for contextual Landmark works, optional `start_here`, further papers, books/chapters, and limitations.
- [ ] Differentiate taxonomy, methodological descent, comparison and applicability by edge styles and clear legend.
- [ ] Pull visualization data from validated `build/atlas-graph.json`, with no independent edited graph database.

## Phase 4 — Ongoing scholarly updates (when invoked)

- [ ] Place new publications in existing method(s), or create a new node only when a genuinely reusable methodological innovation appears.
- [ ] Update recommended starting readings if stronger pedagogical sources appear; preserve valuable old literature as optional.
- [ ] Periodic checking or digests only through explicitly configured automations, if wanted.
- [ ] Optional user-specific reading progress and duplicate-free cross-node reading routes, separate from public scholarly metadata.

The goal is **an expanding map and a small immediate reading load**. Editorial `status`, contextual `significance`, and user-specific reading progress are intentionally independent.
