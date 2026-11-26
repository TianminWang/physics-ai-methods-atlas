# Physics AI Methods Atlas · 物理 AI 方法知识图谱

**[简体中文（default）](README.md) | [English](README.en.md)**

> A growing, evidence-linked knowledge graph of **ODE/PDE inverse problems, scientific ML, neural operators, coronary hemodynamics, personalized digital twins and world models**.

The current design is **one three-phase research axis plus one global method-evolution DAG**. The research axis describes scientific capabilities; the DAG describes documented technical development and its targeted bottlenecks.

## v0.9 methodology structure audit (current research phase)

**Audit the ontology before adding relationships or changing the browser.** The current catalog includes 61 methods, 34 families, 15 research problems and 530 typed links, but combines formulations, algorithm families, concrete numerical methods, model architectures, training strategies, physical models and software frameworks at the same `method.*` level.

We propose a separate cross-application **Capability** layer to connect the three scientific phases to methods and problem scenarios, while preserving independent method-family taxonomy, evidence-backed evolution and the existing single source of scholarly truth.

- [Methodological audit & ontology summary](docs/en/METHODOLOGY_AUDIT_V09.md)
- [Detailed Chinese source-grounded audit](docs/zh/AUDIT_V09.md)
- [Chinese ontology proposal](docs/zh/ONTOLOGY_V09.md)
- [Provisional classification of all 61 methods](audits/v09/method-kind-proposals.json)
- [19 candidate research capabilities](audits/v09/capability-layer-proposal.json)
- [Literature-backed relation review queue](audits/v09/relation-review-queue.json)

**No changes to canonical `data/`, relations, or v0.8 viewer in this phase.** v0.8 remains the latest interactive prototype.

## Three research phases

| Phase | Main question | Child capabilities |
|---|---|---|
| **I. Physical modeling & forward problems** | How do physical laws, parameters and conditions produce states and measurements? | Governing and forward models; observations and data acquisition |
| **II. Inverse problems & inference** | What unknown information can be recovered from sparse noisy observations? | Parameter inference, state estimation, regularization and identifiability |
| **III. Personalized prediction, intervention & updating** | How can individualized models forecast, evaluate interventions and update from new data? | Prediction, counterfactual decision-making, continual assimilation |

Digital twins and world models are relevant system-level directions, not synonyms for the entire third phase. Physical validity, uncertainty, model error and generalization are cross-cutting concerns. Feedback may revise both inference and forward models.

## A relationship-ranked global method graph

The viewer no longer forces methods into six category rectangles. **The v0.8 main SVG ranks methods participating in documented `extends` or `combines` links; other canonical methods remain in a searchable shelf.** Disconnected components are legitimate; no artificial scholarly genealogy is added.

**Node color = technical paradigm:** classical numerics/optimization, statistical/probabilistic, machine/deep learning, or physics–data hybrid. The color is a primary visual tag, not a unique scholarly parent; nonexclusive method-family memberships remain intact.

**Directed edge color = target research phase:** I blue, II purple, III teal, or neutral when unresolved. Extensions and combinations have different line patterns. Taxonomic and comparison links cannot be mistaken for demonstrated improvements.

Nodes and SVG links are equally selectable. Their details show mechanisms, original method-family memberships, actual bottlenecks, trade-offs, source papers, contextual Landmark roles and optional Start Here readings. Stage-to-family relevance remains distinct from method-specific empirical evidence.

## v0.8 full-width evidence-first graph (current)

[Design / usage (English)](docs/en/LAYOUT_V08.md) · [中文版](docs/zh/LAYOUT_V08.md)

The graph now uses nearly the whole page width and a viewport-relative height, with fullscreen mode, an interactive minimap, evolution-component navigation, upstream/downstream focus, global search, and a closeable/pinnable evidence drawer.

The main SVG prioritizes methods with **documented extends/combines evidence**; methods without a recorded evolution link remain in a collapsible, searchable shelf. This is a UI organization decision, **not a claim that those methods lack scientific references**. No artificial edges were added to force a connected graph.

[Download the portable v0.8 viewer from the latest successful GitHub Actions run](https://github.com/TianminWang/physics-ai-methods-atlas/actions/workflows/validate.yml) (artifact: `atlas-fullwidth-dag-v08`). Unzip and open `index.html` offline.

## v0.7 interactive prototype (historical)

[Design specification](docs/en/THREE_PHASE_DAG_V07.md) · [中文说明](docs/zh/THREE_PHASE_DAG_V07.md)

From [GitHub Actions → latest successful Validate atlas data → Artifacts](https://github.com/TianminWang/physics-ai-methods-atlas/actions/workflows/validate.yml), download `atlas-global-dag-v07`, unzip it and open `index.html`. You do not need Graphviz or a web server to view the generated artifact.

This is an **offline testable prototype**, not yet the final GitHub Pages deployment.

## Indexed academic content and reading strategy

Current Atlas: approximately **61 methods, 34 families, 58 paper records, 12 books and 15 scientific problems**, plus typed relationships. The method map is not claimed exhaustive.

- [Method genealogy v0.4 (English)](docs/en/METHOD_GENEALOGY_V04.md)
- [Minimal reading guide](docs/READING_GUIDE.md)
- [Project roadmap](docs/ROADMAP.md)

Landmark significance is contextual to a paper's contribution to a specific method. **Start Here is optional** and has no compulsory paper quota.

## Development

Canonical scholarship lives in `data/`; presentation metadata in `config/v07.json`, latest builder in `scripts/build_v08.py`, and viewer source in `viewer-v08/`. Previous releases remain available.

```bash
python -m pip install -r requirements-dev.txt
python -m scripts.validate
python -m pytest -q
python -m scripts.build_v08 --site build/viewer-v08
```

Graphviz `dot` and a CJK font are needed to **build**, but not to open the generated offline viewer. Historical [v0.6](viewer-v06/README.md) and [v0.5](prototype/README.md) prototypes remain accessible.
