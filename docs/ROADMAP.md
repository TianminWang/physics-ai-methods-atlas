# Roadmap · 项目分阶段建设计划

## Phase 1 — Foundation v0.1 (this Pull Request)

Acceptance criteria:

- [x] Stable entity IDs, separate Method / Paper / Book / Problem / Area / Relation records.
- [x] Type-safe graph links, evidence provenance and designated acyclic subgraphs.
- [x] **1–2 verified must-read papers per curated method**; draft nodes are visibly incomplete.
- [x] Small seed for PINN, DeepONet, FNO, and selected classical-method drafts.
- [x] Cross-file semantic validation, regression tests and derived graph JSON export.
- [x] Curation rules, source-of-truth policy, usage instructions and view planning.
- [ ] Interactive website / large literature corpus (intentionally later phases).

## Phase 2 — Method and literature population

- Build a reliable initial backbone of about 15–25 method nodes, including classical optimization, adjoints, regularization, PINN, DeepONet, FNO, physics-informed operators, learned-forward inversion, Bayesian inverse methods and data assimilation.
- Verify venues, authors, original publications and scholarly lineage; distinguish original contributions, independent evaluations and application studies.
- Give each *curated* method a tight **1–2 paper minimum reading set**; keep all other papers optional.
- Attach books/chapters and high-value coronary inverse-problem case studies.
- Expand typed relationships without pretending a chronological improvement always implies technical superiority.

## Phase 3 — Interactive knowledge graph

- GitHub README presents an accessible overview and a link to the viewer.
- GitHub Pages shows searchable/zoomable/filterable default **method-evolution forest (A)**.
- Provide **research problem / digital-twin pipeline view (B)** and optional **learning dependency view (C)** from the **same validated data**.
- Show must-read papers first, further papers/books second, and make editorial/verification status visible.
- Build visualization from the generated graph JSON rather than maintaining separate visual databases.

## Phase 4 — Ongoing scholarly maintenance

- Triage new publications, update existing method nodes or add a genuinely new method only when warranted.
- Revisit core-paper choices as stronger tutorials or studies appear; preserve the old paper as further reading.
- Integrate explicitly requested periodic searches or scheduled tasks if monitoring becomes useful.
- Keep user-specific reading status separate from the public methodological truth.

The Atlas is a versioned, evolving knowledge base. Changes to the schema require reviewed migrations; routine new papers and method links do not.
