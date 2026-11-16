# Physics AI Methods Atlas · 物理 AI 方法图谱

> A living, evidence-linked **methods atlas** for scientific computing, ODE/PDE inverse problems, neural operators, coronary hemodynamics, and patient-specific digital twins.

**Our goal is not to collect every paper.** We want to understand *what each method does, where it came from, what changed, and when it is useful*. The default mental model is a **method-evolution forest** projected from a typed knowledge graph; a research-problem view will be built from the **same data**.

**核心阅读原则：每个已经整理完成（curated）的方法节点只选 1–2 篇必读论文。** 其他关联论文作为可选扩展，不要求全部阅读。未完成文献筛选的节点明确标记为 draft。

## Current status — foundation v0.1 (2026-11-16)

- **5** scope areas, **7** method nodes (**3 curated**, **4 draft**)
- **3** verified landmark papers and **1** living online book
- **2** example research problems, **22** typed relationships
- JSON Schema, graph integrity and reading-policy validator, and normalized graph exporter
- **Not yet built:** full literature corpus, interactive GitHub Pages site, and automated literature discovery. These belong to later stages.

### Explore the seed catalog

| Curated method | Required paper | What to focus on |
|---|---|---|
| [PINN](data/methods/pinn.json) | [Raissi et al. (2019)](data/papers/raissi-2019-pinn.json) | PDE residuals, forward/inverse formulations |
| [DeepONet](data/methods/deeponet.json) | [Lu et al. (2021)](data/papers/lu-2021-deeponet.json) | Branch/trunk structure and operator maps |
| [FNO](data/methods/fno.json) | [Li et al. (ICLR 2021)](data/papers/li-2021-fno.json) | Fourier layers and parameterized PDEs |

The seed catalog validates the **architecture and reading workflow**, not comprehensive scholarly coverage. See [the reading policy](docs/READING_POLICY.md).

## Canonical data structure

~~~text
data/
  areas/       # scope / view filters (not methodological ancestry)
  methods/     # one method record per node; core_reading lives here
  papers/      # one bibliographic record per paper; reusable across methods
  books/       # books and textbooks; chapter-level coverage is linked
  problems/    # inverse problems / coronary or digital-twin research use cases
  relations/   # typed, evidence-aware directed links
schemas/
  atlas.schema.json  # JSON Schema draft 2020-12, schema_version=1.0.0
scripts/
  validate.py        # cross-record validation + reading-policy checks
  export_graph.py    # normalized graph JSON for a future viewer
tests/               # integrity regression tests
docs/                # architecture, curation policy, contributions, roadmap
~~~

**Single source of truth:** edit records and relationships, **not** manually maintained graph drawings. One paper can connect to several methods. Books can span multiple methods or research areas. Relationships have explicit types: *belongs_to*, *specializes*, *extends*, *combines*, *addresses*, *introduces*, *covers*.

### Locally validate and export

Requires Python 3.11+.

~~~bash
python -m pip install -r requirements-dev.txt
python -m scripts.validate
python -m pytest -q
python -m scripts.export_graph --output build/atlas-graph.json
~~~

Generated exports are deliberately excluded from Git. The interactive visualization is planned for Phase 3, with **method-forest as default** and **research-workflow as switchable view**.

## Design documents

- [Architecture and typed graph semantics](docs/ARCHITECTURE.md)
- [Must-read policy: 1–2 papers per curated method](docs/READING_POLICY.md)
- [Adding papers, methods, books, and evidence claims](docs/CONTRIBUTING.md)
- [Phases and acceptance criteria](docs/ROADMAP.md)

## Scope and standards

Traditional numerical methods and learning-based methods are **peers**, not separate catalogues. The atlas prioritizes ODE/PDE forward solvers, inverse problems, Physics AI, data assimilation & uncertainty, and world models & intervention planning. Coronary hemodynamics is a central use case, not the only allowable domain.

An arrow represents a *specific* claim (e.g., classification, extension, application), **not** proof that one technique is universally better. Claims of lineage require evidence. Mathematical background is documented **as needed per method**, not as a separate obligation to relearn a complete mathematics curriculum.

This is an evolving research aid; original publications remain authoritative.
